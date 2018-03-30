# -*- coding: utf-8 -*-
import pycurl
import urllib
import StringIO
import json
from testdata import *
from bitcoin import ecdsa_raw_sign


# next, you sign the data returned in the tosign array locally
# here we're using our signer tool (https://github.com/blockcypher/btcutils/tree/master/signer), but any ECDSA secp256k1 signing tool should work (Ethereum uses the same ECDSA curve as Bitcoin for transaction signatures)
# $PRIVATEKEY here is a hex-encoded private key corresponding to the input from address add42af7dd58b27e1e6ca5c4fdc01214b52d382f


def initCurl():
    c = pycurl.Curl()
    c.setopt(pycurl.COOKIEFILE, "cookie_file_name")  # 把cookie保存在该文件中
    c.setopt(pycurl.COOKIEJAR, "cookie_file_name")
    c.setopt(pycurl.FOLLOWLOCATION, 1)  # 允许跟踪来源
    c.setopt(pycurl.MAXREDIRS, 5)
    # 设置代理 如果有需要请去掉注释，并设置合适的参数
    # c.setopt(pycurl.PROXY, ‘http://11.11.11.11:8080′)
    # c.setopt(pycurl.PROXYUSERPWD, ‘aaa:aaa’)
    return c


def GetData(curl, url):
    head = ['Accept:*/*',
            'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11']
    buf = StringIO.StringIO()
    curl.setopt(pycurl.WRITEFUNCTION, buf.write)
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, head)
    curl.perform()
    the_page = buf.getvalue()
    buf.close()
    return the_page


# 提交数据到url，这里使用了HTTP的POST方法

# 备注，这里提交的数据为json数据，
# 如果需要修改数据类型，请修改head中的数据类型声明
def PostData(curl, url, data):
    head = ['Accept:*/*',
            'Content-Type:application/xml',
            'render:json',
            'clientType:json',
            'Accept-Charset:GBK,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding:gzip,deflate,sdch',
            'Accept-Language:zh-CN,zh;q=0.8',
            'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11']
    buf = StringIO.StringIO()
    curl.setopt(pycurl.WRITEFUNCTION, buf.write)
    # data = urllib.urlencode(data)
    curl.setopt(pycurl.POSTFIELDS, data)
    curl.setopt(pycurl.URL, url)
    # curl.setopt(pycurl.HTTPHEADER, head)
    curl.perform()
    the_page = buf.getvalue()
    # print the_page
    buf.close()
    return the_page


def test():
    Token = "5003504c53a84e5290778d69f1930a10"
    c = initCurl()
    html = GetData(c,
                   'https://api.blockcypher.com/v1/eth/main/txs/8f39fb4940c084460da00a876a521ef2ba84ad6ea8d2f5628c9f1f8aeb395342')
    print html

    data = '{"inputs": [{"addresses": ["1cc60c94254c0f0f0b957fb7c3dfed2d00e49a4c"]}],\
            "outputs": [{"addresses": ["add42af7dd58b27e1e6ca5c4fdc01214b52d382f"], "value": 4200000000000000}]}'

    html = PostData(c, 'https://api.blockcypher.com/v1/eth/main/txs/new?token=5003504c53a84e5290778d69f1930a10', data)
    print html

    url = 'https://api.blockcypher.com/v1/eth/main/addrs'
    html = PostData(c, url, '')
    # curl.setopt(pycurl.POSTFIELDS, '')
    # curl.setopt(pycurl.URL, url)
    #
    # curl.perform()
    # the_page = buf.getvalue()
    print html


# test()

import blockcypher
from bitcoin import der_encode_sig

def make_tx_signatures(txs_to_sign, privkey):
    signatures = []
    for tx_to_sign in txs_to_sign:
        sig = der_encode_sig(*ecdsa_raw_sign(tx_to_sign.rstrip(' \t\r\n\0'), privkey))
        signatures.append(sig)
    return signatures



def testsign():
    data = '{"inputs":[{"addresses": ["%s"]}],' \
           '"outputs":[{"addresses": ["%s"], ' \
           '"value": 1}]}'%myaddress1['address'],myaddress2['address']

    url='https://api.blockcypher.com/v1/beth/test/txs/new?token=5003504c53a84e5290778d69f1930a10'
    c = initCurl()
    html = PostData(c, url, data)
    print html

    unsigned_tx = json.loads(html)



    # unsigned='646b5cc387cef8ced58d861c2ddae75568b4936ccb2971371a0f9d2321460381'
    # privkey_list = 'b3bd48cbfc88ddcaa9b600c90a62a07fe6c27503ae5b4872c041e5aecf2e723d'
    # pubkey_list = ['0496a0747fcd0af86661c34867e9d05214f55c87b90e4c97cf20e8ab14ece4a1a9b724f0dd328d8fd9bb6af81965a57f47bf62066a20bbce532ea32fdbcecacdc1']


    tx_signatures = make_tx_signatures(txs_to_sign=unsigned_tx['tosign'], privkey=privkey_list)

    unsigned_tx["signatures"]=tx_signatures

    print unsigned_tx
    kky = json.dumps(unsigned_tx)
    print kky

    data=kky
    html = PostData(c, 'https://api.blockcypher.com/v1/beth/test/txs/send?token=5003504c53a84e5290778d69f1930a10', data)
    print html


#testsign()

data = '{"inputs":[{"addresses": ["%s"]}],' \
           '"outputs":[{"addresses": ["%s"], ' \
           '"value": 1}]}'%(myaddress1['address'],myaddress2['address'])
print data

# c = pycurl.Curl()
# c.setopt(pycurl.URL, 'https://api.blockcypher.com/v1/beth/test/blocks/5;6;7')
#
# b = StringIO.StringIO()
# c.setopt(pycurl.WRITEFUNCTION, b.write)
# c.perform()
# # print b.getvalue()
#
# crl = pycurl.Curl()
# crl.fp = StringIO.StringIO()
# url = "https://api.blockcypher.com/v1/beth/test/faucet?token=%s" % Token
# post_data_dic = {"address": "1585a07efe60806132c994eb39b5f33f55a1eff8", "amount": 1000000000000000000}
# # crl.setopt(pycurl.POSTFIELDS, urllib.urlencode(post_data_dic))
# crl.setopt(pycurl.POSTFIELDS)
# crl.setopt(pycurl.URL, url)
# crl.setopt(pycurl.WRITEFUNCTION, crl.fp.write)
# crl.perform()
# print crl.fp.getvalue()
