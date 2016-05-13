#coding:utf-8
sFiles="odnsodbsocosoddsodbsmasmasmasmbsmesmbseusensmbsetsmnstmsadstosocmsodnsodb\
socosoddsodbsmasmasmasedsmesedsecseoseusmasmnstmsadstosocmsodnsodbsocosoddsodbsma\
smasmaseosmesedsmbsecsedsetsmnstmsadstosocmsodnsodbsocosoddsodbsmasmasmasecsmesem\
smbsmbseeseosmnstmsadstosocmsodnsodbsocosoddsodbsmasmasmaseusmesensedsecseusemsmn\
stmsadstosocmsodnsodbsocosoddsodbsmasmasmasemsmesmbsensetseuseosmnstmsadstosocmso\
dnsodbsocosoddsodbsmasmasmaseesmesmbsenseesensedsmnstmsadstosocmsodnsodbsocosodds\
odbsmasmasmasensmesemsemsedsemsensmnstmsadstosocmsodnsodbsocosoddsodbsmasmasmaset\
smesecsecsmbsmaseusmnstmsadstosocmsodnsodbsocosoddsodbsmasmasmbsmasmesetsemsemsmb\
sensmnstmsadstosocmsodnsodbsocosoddsodbsmasmasmbsmbsmesmbsedsecseusetsmnstmsadsto\
socmsodnsodbsocosoddsodbsmasmasmbsedsmesmbsetsetseesedsmnstmsadstosocmsodnsodbsoc\
osoddsodbsmasmasmbseosmeseusmasemseosmasmnstmsadstosocmsodnsodbsocosoddsodbsmasma\
smbsecsmesemseoseosensetsmnstmsadstosocmsodnsodbsocosoddsodbsmasmasmbseusmesmbsee\
senseuseusmnstmsadstosocmsodnsodbsocosoddsodbsmasmasmbsemsmesedsmasenseosmbsmnstm\
sadstosocmsodnsodbsocosoddsodbsmasmasmbseesmesmbsmasensemsecsmnstmsadstodocumenta\
bsceaadsf"
#x = 'e'
x = sFiles[len(sFiles)-1:] # x = 'e'
d = "abcdefghijklmnopqrstuvwxyz".index(x) + 1 # d = '5'
#e = 'documentabs'
e = sFiles[len(sFiles)-d-12:len(sFiles)-d-1] # e = 'documentabs'
s = sFiles[:len(sFiles)-d-12]
k = e[:len(e)-1] # k = 'documentab'
"""
s=s.replace(/d/g,'0')
s=s.replace(/o/g,'1')
s=s.replace(/c/g,'2')
s=s.replace(/u/g,'3')
s=s.replace(/m/g,'4')
s=s.replace(/e/g,'5')
s=s.replace(/n/g,'6')
s=s.replace(/t/g,'7')
s=s.replace(/a/g,'8')
s=s.replace(/b/g,'9')
"""
f = e[-1]
for i in range(len(k)):
    s =  s.replace(k[i], str(i))
#print sFiles
g = s.split(f)
#print g
gif = ""
for num in g:
    gif += chr(int(num))

gifs = gif.split('|')

print gifs

