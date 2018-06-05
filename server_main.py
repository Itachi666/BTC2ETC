# ETHaddress = {
#     "private": "0b481a44ff33a78ff446b647cf30d3b7a69b8cfdf8bfcec5d54fcecbe5ed5808",
#     "public": "0478e977bff6a819b79e3c1fc59ffec45cb80e6fc970d63afb0341b22d85e9ead034dd2ba39df0808ec1e02c0358daf8f99be33882b49ebf3c082796ea7b1bc0a8",
#     "address": "ad924bce5b3550190ce983bc671219b3d53955c4"
# }
#
# BTCaddress = {
#     "private": "1894f0cc32e6288f981594768a07e86f1bc6653e43481e1b86493a98469d1e4f",
#     "public": "03af6dd2c932454ba7896dffc515d1058726bc6c95b5fd941abcae44bb46d3b78c",
#     "address": "CCVjieoayAy9YzGSmRpezAv6LFDQmdkedT",
#     "wif": "Bp9pCWBWvmLS8Coix1mhv29Tpfk5rKAj9srRmfCAvncpaFTD26k6"
# }
import ETH.ETH
import BTC.BTC
import server.superuser
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import json

Adm = server.superuser.SuperUser("BigBoss")
BigBoss = {}

btc2usd = 5.0
eth2usd = 1.0


class send(Resource):
    def get(self, option):
        pass

    def put(self, option):
        data = request.form['data']
        BigBoss = json.loads(data)
        if option == 'ETH':
            html = ETH.ETH.send_tx(data)
            BTC.BTC.send_tx(Adm.btctx)
            Adm.btctx=''
            return html
        if option == 'BTC':
            html = BTC.BTC.send_tx(data)
            ETH.ETH.send_tx(Adm.ethtx)
            Adm.ethtx=''
            return html


class new(Resource):
    def get(self):
        return "happy"

    def put(self):
        data = request.form['data']
        print data
        BigBoss = json.loads(data)


        if BigBoss["input"] == "BTC":
            input = BTC.BTC.getbalance(BigBoss["inputaddress"])
            if (input["final_balance"] < BigBoss["value"]):
                return "Do not have enough money!"
            if BigBoss["output"] == "BTC":
                return BigBoss["outputaddress"]
            if BigBoss["output"] == "ETH":
                # check outputaddress
                v = int(btc2usd / eth2usd * BigBoss["value"])
                Adm.ethtx = Adm.ethereum.make_tx_and_sign(output=BigBoss["outputaddress"], value=v)
            return Adm.bitcoin.address["address"]



        if BigBoss["input"] == "ETH":
            input = ETH.ETH.getbalance(BigBoss["inputaddress"])
            if (input["final_balance"] < BigBoss["value"]):
                return "Do not have enough money!"

            if BigBoss["output"] == "ETH":
                return BigBoss["outputaddress"]

            if BigBoss["output"] == "BTC":
                # check outputaddress
                v = int(eth2usd / btc2usd * BigBoss["value"])
                Adm.btctx = Adm.bitcoin.make_tx_and_sign(output=BigBoss["outputaddress"], value=v)

            return Adm.ethereum.address["address"]


def main():
    # Adm.getbalance()
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(send, '/send/<string:option>')
    api.add_resource(new, '/new/')
    app.run(debug=True)


if __name__ == "__main__":
    main()
