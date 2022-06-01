import re

string = 'the articles about Will Smith'
string2 = 'will smith on news'
string3 = 'the News about will smith'
string4 = 'news about will smith'
string5 = 'nothing left to lose'
string6 = 'golden boots on this year'

keyword = string6
check = keyword
print(check)
p = re.compile('([tT]he |[oO]n |[aA][nN]* )*([aA][rR][tT][iI][cC][lL][eE][sS]*|[nN][eE][wW][sS])+( [aA]bout| [oO]f)*')
c = list(p.findall(check))
if len(c) > 0:
    for pattern in c:
        pattern = ''.join(list(pattern))
        keyword = re.sub(pattern, '', keyword)
print(keyword)
