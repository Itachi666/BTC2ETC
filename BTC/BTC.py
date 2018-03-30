import SkPk
import CURL
import json
from blockcypher import send_faucet_coins
from blockcypher import get_address_details
from blockcypher import get_address_overview


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
        data=get_address_overview(self.address["address"],coin_symbol='bcy')
        return data["final_balance"]

    def showmethemoney(self):
        send_faucet_coins(address_to_fund=self.address["address"], satoshis=10000, api_key=Token,
                          coin_symbol='bcy')




def get_address():
    c = CURL.initCurl()
    url = 'https://api.blockcypher.com/v1/bcy/test/addrs?token=%s' % Token
    html = CURL.PostData(c, url, '')
    return html


