import SkPk
import CURL
import json
from blockcypher import send_faucet_coins
from blockcypher import get_address_details
from blockcypher import get_address_overview
from blockcypher import make_tx_signatures

from bitcoin import der_encode_sig
from bitcoin import ecdsa_raw_sign

Token = '5003504c53a84e5290778d69f1930a10'


# {
#   "private": "1894f0cc32e6288f981594768a07e86f1bc6653e43481e1b86493a98469d1e4f",
#   "public": "03af6dd2c932454ba7896dffc515d1058726bc6c95b5fd941abcae44bb46d3b78c",
#   "address": "CCVjieoayAy9YzGSmRpezAv6LFDQmdkedT",
#   "wif": "Bp9pCWBWvmLS8Coix1mhv29Tpfk5rKAj9srRmfCAvncpaFTD26k6"
# }


class BTC_wallet():
    def __init__(self):
        self.address = {}

    def setaddress(self):
        self.address = json.loads(get_address())

    def haveaddress(self, private, public, address):
        self.address["private"] = private
        self.address["public"] = public
        self.address["address"] = address
        self.address["wif"] = SkPk.getWIF(private + '01')  # it is different between testnet and main net

    def getbalance(self):
        data = get_address_overview(self.address["address"], coin_symbol='bcy')
        return data

    def showmethemoney(self):
        print send_faucet_coins(address_to_fund=self.address["address"], satoshis=100000000, api_key=Token,
                                coin_symbol='bcy')

    def make_tx_and_sign(self, output, value):
        unsigned_tx = create_tx(self.address["address"], output, value)
        unsigned_tx["signatures"], unsigned_tx["pubkeys"] = make_tx_signatures(txs_to_sign=unsigned_tx['tosign'],
                                                                               privkey=self.address["private"],
                                                                               pubkey=self.address["public"])

        data = json.dumps(unsigned_tx)
        #print json.dumps(unsigned_tx, sort_keys=False, indent=4, separators=(',', ':'))
        return data


def get_address():
    c = CURL.initCurl()
    url = 'https://api.blockcypher.com/v1/bcy/test/addrs?token=%s' % Token
    html = CURL.PostData(c, url, '')
    return html


def getbalance(address):
    data = get_address_overview(address, coin_symbol='bcy')
    return data


def send_tx(data):
    c = CURL.initCurl()
    url = 'https://api.blockcypher.com/v1/bcy/test/txs/send?token=%s' % Token
    html = CURL.PostData(c, url, data)
    return html


def make_tx_signatures(txs_to_sign, privkey, pubkey):
    signatures = []
    public = []
    for tx_to_sign in txs_to_sign:
        sig = der_encode_sig(*ecdsa_raw_sign(tx_to_sign.rstrip(' \t\r\n\0'), privkey))
        signatures.append(sig)
        public.append(pubkey)
    return signatures, public


def create_tx(input, output, value):
    data = '{"inputs":[{"addresses": ["%s"]}],' \
           '"outputs":[{"addresses": ["%s"], ' \
           '"value": %d}]}' % (input, output, value)

    url = 'https://api.blockcypher.com/v1/bcy/test/txs/new'
    c = CURL.initCurl()
    html = CURL.PostData(c, url, data)
    return json.loads(html)


def make_tx_and_send(myaddress, output, value):
    unsigned_tx = create_tx(myaddress["address"], output, value)
    unsigned_tx["signatures"], unsigned_tx["pubkeys"] = make_tx_signatures(txs_to_sign=unsigned_tx['tosign'],
                                                                           privkey=myaddress["private"],
                                                                           pubkey=myaddress["public"])

    data = json.dumps(unsigned_tx)
    #print json.dumps(unsigned_tx, sort_keys=False, indent=4, separators=(',', ':'))
    send_tx(data)
