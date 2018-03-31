import user
import CURL
import json

from testdata import *


def main():
    username='TBK'
    user1=user.User(username)
    #user1.bitcoin.showmethemoney()
    user1.getbalance()
    #user1.transaction("BTC","ETH","f34a27ce7ba36e93399720e4e43f83183eca4ec2",1000)
    user1.transaction("ETH", "BTC", "CFkbTiXfRe4eHqZ6scF7CQEYKZmLHfqEnK", 1000)


if __name__ == "__main__":
    main()
