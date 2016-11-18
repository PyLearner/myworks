__author__ = 'myang'

import urllib.request
import http.cookiejar
import urllib.parse
cookie = http.cookiejar.MozillaCookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
url = 'http://www.baidu.com'
req = urllib.request.Request(url)
# info = {'name':'myang','age':28}
# info1 = urllib.parse.urlencode(info)
# print(info1)
content = opener.open(req)

cookie.save('d:/cookie.txt')


print(cookie.filename)

