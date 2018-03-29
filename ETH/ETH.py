# -*- coding: utf-8 -*-
from bitcoin import der_encode_sig
from bitcoin import ecdsa_raw_sign
import json
import CURL

from testdata import *

Token = '5003504c53a84e5290778d69f1930a10'

def getbalance(address):
    c = CURL.initCurl()
    html = CURL.GetData(c, 'https://api.blockcypher.com/v1/beth/test/addrs/%s/balance' % address)
    print html


def showmethemoney(address):
    c = CURL.initCurl()
    data = '{"address": "%s", "amount": 1000000000000000000}' % address
    html = CURL.PostData(c, 'https://api.blockcypher.com/v1/beth/test/faucet?token=%s' % Token, data)
    return html


def get_address():
    c = CURL.initCurl()
    url = 'https://api.blockcypher.com/v1/beth/test/addrs?token=%s' % Token
    html = CURL.PostData(c, url, '')
    return html


def send_tx(data):
    c = CURL.initCurl()
    url = 'https://api.blockcypher.com/v1/beth/test/txs/send?token=%s' % Token
    html = CURL.PostData(c, url, data)
    print html


def make_tx_signatures(txs_to_sign, privkey):
    signatures = []
    for tx_to_sign in txs_to_sign:
        sig = der_encode_sig(*ecdsa_raw_sign(tx_to_sign.rstrip(' \t\r\n\0'), privkey))
        signatures.append(sig)
    return signatures


def create_tx(input, output, value):
    data = '{"inputs":[{"addresses": ["%s"]}],' \
           '"outputs":[{"addresses": ["%s"], ' \
           '"value": %d}]}' % (input, output, value)

    url = 'https://api.blockcypher.com/v1/beth/test/txs/new?token=%s' % Token
    c = CURL.initCurl()
    html = CURL.PostData(c, url, data)
    return json.loads(html)


def tx(myaddress, output, value):
    unsigned_tx = create_tx(myaddress["address"], output, value)
    unsigned_tx["signatures"] = make_tx_signatures(txs_to_sign=unsigned_tx['tosign'], privkey=myaddress["private"])

    data = json.dumps(unsigned_tx)
    send_tx(data)

# tx(inputaddress, outputaddress["address"], 1)
getbalance(inputaddress["address"])