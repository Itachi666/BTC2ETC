import test
import BTC.BTC
c=test.initCurl()

data='{"signatures": ["304402203cea35d36ac482c0e98b1ae9741a636a494bf20770953d6f634ef80a45cc7db802206e9acf3fb72993af2ea6051c45cde2803dc14eb15eed3f9cc63e6d8d2c5c810c"], "tosign": ["2d750aa033068d277cc2944cf8e8e4577808655673af3fec52f0356fc149913a"], "tx": {"received": "2018-03-28T12:20:05.004177897Z", "hash": "c5fbe9f7c9dced24fe72b111f26bb1cacfa391dbb4147c95e8d01088a99282ac", "addresses": ["ad924bce5b3550190ce983bc671219b3d53955c4"], "inputs": [{"addresses": ["ad924bce5b3550190ce983bc671219b3d53955c4"], "sequence": 2}], "outputs": [{"addresses": ["884bae20ee442a1d53a1d44b1067af42f896e541"], "value": 0}], "block_height": -1, "block_index": 0, "vin_sz": 1, "vout_sz": 1, "fees": 4830000000000000, "gas_price": 230000000000, "double_spend": false, "total": 0, "ver": 0, "gas_limit": 21000, "size": 37}}'
html = test.PostData(c, 'https://api.blockcypher.com/v1/beth/test/txs/send?token=5003504c53a84e5290778d69f1930a10', data)
print html