# -*- coding: utf-8 -*-
import pycurl
import StringIO


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

# 备注，这里提交的数据为json格式的字符串，
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