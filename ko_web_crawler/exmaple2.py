import re

p = re.compile('^(what is )[A-Za-z0-9]+')
string = 'what is captain america?'
string2 = 'the legend of league'
string3 = 'who is son of abraham?'
p2 = re.compile('[A-za-z0-9 ]+\?$')

m = p.match(string)
print(m)
m = p.match(string2)
print(m)
re.sub('what is', '', string)
re.sub('\?', '', string)
print(string)
print(p2.match(string2))
print(p2.match(string3))
