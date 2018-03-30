import user
import os
import sqlite3
from testdata import *




def main():
    username='TBK'
    user1=user.User(username)
    user1.have_eth("0b481a44ff33a78ff446b647cf30d3b7a69b8cfdf8bfcec5d54fcecbe5ed5808",
               "0478e977bff6a819b79e3c1fc59ffec45cb80e6fc970d63afb0341b22d85e9ead034dd2ba39df0808ec1e02c0358daf8f99be33882b49ebf3c082796ea7b1bc0a8",
               "ad924bce5b3550190ce983bc671219b3d53955c4")

    user1.have_btc("1894f0cc32e6288f981594768a07e86f1bc6653e43481e1b86493a98469d1e4f",
               "03af6dd2c932454ba7896dffc515d1058726bc6c95b5fd941abcae44bb46d3b78c",
               "CCVjieoayAy9YzGSmRpezAv6LFDQmdkedT")
    user1.getbalance()


if __name__ == "__main__":
    main()