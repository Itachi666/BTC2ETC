# -*- coding: utf-8 -*-
import BTC.BTC
import ETH.ETH
import sqlite3
import os
import json


class SuperUser:
    def __init__(self, name):
        self.username = name
        self.bitcoin = BTC.BTC.BTC_wallet()
        self.ethereum = ETH.ETH.ETH_wallet()
        self.initDB()
        self.user_exists()

    def initDB(self):
        if os.path.exists('ServerData.db'):
            self.conn = sqlite3.connect('ServerData.db')
            self.conn.isolation_level = None
        else:
            self.conn = sqlite3.connect('ServerData.db')
            self.conn.isolation_level = None
            self.conn.execute('''CREATE TABLE INFO
                        (Name char(255) PRIMARY KEY NOT NULL,
                        BTC char(8095),
                        ETH char(8095))''')
            self.conn.commit()

        '''
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM INFO')
        self.displayData = cur.fetchall()
        cur.close()
        self.current_row = len(self.displayData)
        '''

    def user_exists(self):
        sql_cmd = '''select * from INFO where Name = '%s' ''' % self.username
        cursor =self.conn.execute(sql_cmd)
        res = cursor.fetchall()
        suc = True
        if len(res) > 0:
            data=res[0]
            bit=json.loads(data[1])
            self.have_btc(bit["private"], bit["public"], bit["address"])
            eth=json.loads(data[2])
            self.have_eth(eth["private"], eth["public"], eth["address"])
            suc = True
        else:
            sql_cmd_2 = '''insert into INFO(Name) values('%s') ''' % self.username
            self.conn.execute(sql_cmd_2)
            self.set_initial_data()
            suc = False
        self.conn.commit()
        return suc

    def set_initial_data(self):
        self.bitcoin.setaddress()
        self.ethereum.setaddress()
        self.conn.execute(
            '''update INFO set BTC='%s' where Name = '%s' ''' % (json.dumps(self.bitcoin.address), self.username))
        self.conn.execute(
            '''update INFO set ETH='%s' where Name = '%s' ''' % (json.dumps(self.ethereum.address), self.username))
        self.conn.commit()

    def have_eth(self, private, public, address):
        self.ethereum.haveaddress(private, public, address)
        self.conn.execute(
            "update INFO set ETH='%s' where Name = '%s'" % (json.dumps(self.ethereum.address), self.username))
        self.conn.commit()

    def have_btc(self, private, public, address):
        self.bitcoin.haveaddress(private, public, address)
        self.conn.execute(
            "update INFO set BTC='%s' where Name = '%s'" % (json.dumps(self.bitcoin.address), self.username))
        self.conn.commit()

    def getbalance(self):
        self.ethbalance = self.ethereum.getbalance()
        print "Your ETH final balance:", self.ethbalance
        self.btcbalance = self.bitcoin.getbalance()
        print "Your BTC final balance:", self.btcbalance




