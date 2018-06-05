# -*- coding: utf-8 -*-
import user
import Tkinter as tk
import tkMessageBox
import ttk
import time

from testdata import *

image_btc = None


class MyDialog(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Input Transaction info')
        # 弹窗界面
        self.setup_UI()
        self.resizable(0, 0)

    def setup_UI(self):
        # 第一行（两列）
        row1 = tk.Frame(self)
        row1.pack(fill="x", ipadx=1, ipady=10)
        tk.Label(row1, text='Input：', width=15).pack(side=tk.LEFT)
        self.input = tk.StringVar()
        tk.Entry(row1, textvariable=self.input, width=30).pack(side=tk.LEFT)

        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill="x", ipadx=1, ipady=10)
        tk.Label(row2, text='value：', width=15).pack(side=tk.LEFT)
        self.value = tk.IntVar()
        tk.Entry(row2, textvariable=self.value, width=30).pack(side=tk.LEFT)

        row3 = tk.Frame(self)
        row3.pack(fill="x", ipadx=1, ipady=10)
        tk.Label(row3, text='Output：', width=15).pack(side=tk.LEFT)
        self.output = tk.StringVar()
        tk.Entry(row3, textvariable=self.output, width=30).pack(side=tk.LEFT)

        row4 = tk.Frame(self)
        row4.pack(fill="x", ipadx=1, ipady=10)
        tk.Label(row4, text='OutputAddress：', width=15).pack(side=tk.LEFT)
        self.outputaddress = tk.StringVar()
        tk.Entry(row4, textvariable=self.outputaddress, width=30).pack(side=tk.LEFT)

        # 第三行
        row5 = tk.Frame(self)
        row5.pack(fill="x")
        tk.Button(row5, text="取消", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row5, text="确定", command=self.ok).pack(side=tk.RIGHT)

    def ok(self):
        self.userinfo = [self.input.get(), self.value.get(), self.output.get(), self.outputaddress.get()]  # 设置数据
        self.destroy()  # 销毁窗口

    def cancel(self):
        self.userinfo = None  # 空！
        self.destroy()


# 主窗


class MyApp(tk.Tk):
    def __init__(self, username='TBK'):
        tk.Tk.__init__(self)

        # 程序参数/数据
        self.table_num = 0
        self.user1 = user.User(username)

        self.btcaddress = self.user1.bitcoin.address["address"]
        self.ethaddress = self.user1.ethereum.address["address"]

        self.refresh_money()

        # 程序界面
        # self.pack() # 若继承 tk.Frame ，此句必须有！
        self.title(username + '\'s Wallet')
        self.geometry('800x500')
        self.setupUI()
        self.resizable(0, 0)

    def setupUI(self):
        global image_btc
        global image_eth
        image_btc = tk.PhotoImage(file='btc.gif')
        image_eth = tk.PhotoImage(file='eth.gif')

        self.canvas1 = tk.Canvas(self, bg='white', height=200, width=200)
        self.canvas1.create_image(0, 0, anchor='nw', image=image_btc)

        self.canvas2 = tk.Canvas(self, bg='white', height=200, width=200)
        self.canvas2.create_image(0, 0, anchor='nw', image=image_eth)

        self.canvas1.place(x=1, y=1, anchor='nw')
        self.canvas2.place(x=799, y=1, anchor='ne')

        self.frame_btc = tk.Frame(self, width=398, height=100)
        self.frame_eth = tk.Frame(self, width=398, height=100)

        self.left_btc = tk.Label(self.frame_btc, text="BTC:", font=('Monaco', 20)).place(x=0, y=1, anchor='nw')
        self.left_btcaddress = tk.Label(self.frame_btc, text=self.btcaddress,
                                        font=('Monaco', 12)).place(x=1, y=40, anchor='nw')

        self.right_eth = tk.Label(self.frame_eth, text="ETH:", font=('Monaco', 20)).place(x=398, y=1, anchor='ne')
        self.right_ethaddress = tk.Label(self.frame_eth, text=self.ethaddress,
                                         font=('Monaco', 11)).place(x=398, y=40, anchor='ne')

        self.frame_btc.place(x=201, y=0, anchor='nw')
        self.frame_eth.place(x=201, y=100, anchor='nw')

        self.ethbutton = tk.Button(self, text='Get Balance', font=('Monaco', 8), width=12, height=1,
                                   command=self.showeth).place(x=50, y=202,
                                                               anchor='nw')

        self.btcbutton = tk.Button(self, text='Get Balance', font=('Monaco', 8), width=12, height=1,
                                   command=self.showbtc).place(x=650, y=202,
                                                               anchor='nw')

        self.transactionbutton = tk.Button(self, text='Start a Transaction', font=('Monaco', 15), width=30, height=1,
                                           bg='green',
                                           command=self.start_transaction).place(x=220, y=200,
                                                                                 anchor='nw')

        self.settable()

    def settable(self):
        self.frame_table = tk.Frame(self, width=800, height=250)
        # 创建表格
        self.tree_date = ttk.Treeview(self.frame_table, height=10, show="headings")
        # 定义列
        self.tree_date['columns'] = ['num', 'time', 'in', 'value', 'out', 'outaddress', 'buff']
        self.tree_date.pack(side='bottom')
        # 设置列宽度
        self.tree_date.column('num', width=40, anchor='center')
        self.tree_date.column('time', width=100, anchor='center')
        self.tree_date.column('in', width=75, anchor='center')
        self.tree_date.column('value', width=75, anchor='center')
        self.tree_date.column('out', width=75, anchor='center')
        self.tree_date.column('outaddress', width=300, anchor='center')
        self.tree_date.column('buff', width=75, anchor='center')

        # 添加列名
        self.tree_date.heading('num', text='编号')
        self.tree_date.heading('time', text='发起时间')
        self.tree_date.heading('in', text='输入币种')
        self.tree_date.heading('value', text='转账金额')
        self.tree_date.heading('out', text='输出币种')
        self.tree_date.heading('outaddress', text='输出地址')
        self.tree_date.heading('buff', text='状态')

        self.vbar = ttk.Scrollbar(self.frame_table, orient=tk.VERTICAL, command=self.tree_date.yview)
        self.tree_date.configure(yscrollcommand=self.vbar.set)
        self.tree_date.grid(row=0, column=0, sticky=tk.NSEW)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)

        self.frame_table.place(x=20, y=260, anchor='nw')

        self.add_table_data(['BTC', 3154, 'ETH', 'f34a27ce7ba36e93399720e4e43f83183eca4ec2'])
        self.add_table_data(['ETH', 2233, 'BTC', 'CFkbTiXfRe4eHqZ6scF7CQEYKZmLHfqEnK'])

    def add_table_data(self, data):
        nowtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.tree_date.insert('', self.table_num,
                              values=[self.table_num + 1, nowtime, data[0], data[1], data[2], data[3], 'Success'])
        self.table_num += 1

    def refresh_money(self):
        self.ethinfo, self.btcinfo = self.user1.getbalance()

    def showeth(self):
        tkMessageBox.showinfo(title='ETH Balance',
                              message='Your ETH final balance is ' + str(
                                  self.ethinfo["final_balance"] / 1000000000000000000.0))

    def showbtc(self):
        tkMessageBox.showinfo(title='BTC Balance',
                              message='Your BTC final balance is ' + str(self.btcinfo["final_balance"] / 100000000.0))

    # 设置参数
    def start_transaction(self):
        # 接收弹窗的数据
        res = self.ask_userinfo()
        print(res)
        if res is None:
            return
        # 更改参数
        input, value, output, outputaddress = res

        self.user1.transaction(input, output, outputaddress, value)

        # 更新界面
        nowtime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        data = [input, value, output, outputaddress]
        self.add_table_data(data)

    # 弹窗
    def ask_userinfo(self):
        inputDialog = MyDialog()
        self.wait_window(inputDialog)  # 这一句很重要！！！
        return inputDialog.userinfo


def main():
    # username = raw_input('Username: ')
    username = 'TBK'

    app = MyApp(username)
    app.mainloop()

    # print user1.ethereum.showmethemoney()
    # user1.getbalance()
    # user1.transaction("BTC", "ETH", "f34a27ce7ba36e93399720e4e43f83183eca4ec2", 1000)
    # user1.transaction("ETH", "BTC", "CFkbTiXfRe4eHqZ6scF7CQEYKZmLHfqEnK", 1000)


if __name__ == "__main__":
    main()
