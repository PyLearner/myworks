__author__ = 'myang'
import re

str = 'Paris in the 22 the spring'

m=re.match('([abc])+','abc')
print(m.group(1))
print(m.groups())