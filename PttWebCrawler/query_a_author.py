# -*- coding: utf-8 -*-
import getpass
import telnetlib
import re

'''
# followings: are avialable site
host = "zombiemud.org"
port = 23 
'''
host = "ptt.cc"
port = 443
'''
user = raw_input("Enter your remote account: ")
password = getpass.getpass()
'''
user = "kyopc"
password = "2566353"
match_str1 = u"註冊: ".encode("big5")
match_str2 = u"請輸入您的密碼: ".encode("big5")
match_str3 = u"請按任意鍵繼續".encode("big5")
match_str4 = u"呼叫器".encode("big5")
match_str5 = u"請輸入使用者代號: ".encode("big5")
match_str6 = match_str3
match_extra_str1 = u"請勿頻繁登入".encode("big5")

'''
# reference: https://www.ptt.cc/bbs/Python/M.1364380345.A.27E.html
'''
'''
tn.expect will return a tuple of 3 items.
The first item will be -1 if timeout (not match)
'''

print "start to connect"
tn = telnetlib.Telnet(host)

tn.expect([match_str1], 10)
print "match str1"
tn.write(user + "\r")

tn.expect([match_str2])
print "match str2"
tn.write(password + "\r")

too_often_login = tn.expect([match_extra_str1], 3)
if too_often_login[0] == -1:
    print "not too often login"
    # IMPORTANT !!! Send Ctrl+L (\x0C)  to tell server resent text
    # reference 1 :  http://donsnotes.com/tech/charsets/ascii.html
    # reference 2 :  https://www.ptt.cc/bbs/Python/M.1364380345.A.27E.html
    tn.write('\x0C')
else:
    print "login too often !!!"
    tn.write(" ")

tn.expect([match_str3])
print "match str3"
tn.write(" ")
# entering "query user"
tn.expect([match_str4])
print "match str4"
tn.write("t" + "\r" + "q" + "\r")

# entering "PTT ID"
tn.expect([match_str5])
print "match str5"
tn.write("was599" + "\r")

#tn.expect([match_str6])
result = tn.read_until(match_str6)
result = result.decode('big5')
print "match str6"
tn.close()


# TODO: matching "《有效文章》"
'''
Let's play encoding
'''
'''
use this article to see big5 in vim:
https://blog.xuite.net/smes.pc/blog/32122095-%E8%A7%A3%E6%B1%BA+vim+%E7%9A%84%E3%80%8C%E7%B7%A8%E7%A2%BC%E3%80%8D%E5%95%8F%E9%A1%8C
'''
with open("ptt_id_info.txt", 'wb') as f:
    f.write(result.encode('big5'))
	
