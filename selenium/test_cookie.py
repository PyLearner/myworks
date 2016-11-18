__author__ = 'myang'

import urllib.request
import http.cookiejar
import urllib.parse
url = 'http://www.baidu.com'
file = r'd:/cookie.txt'

cj = http.cookiejar.MozillaCookieJar()
cj.revert(file)
print('before', cj)
# print(cj.filename)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
req = urllib.request.Request(url)
f = opener.open(req)
print(f.geturl())
print(f.getcode())
print(f.info())
print(urllib.request.pathname2url('d:/vrrrp.jpg'))
