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
user = raw_input("Enter your remote account: ")
password = getpass.getpass()
ptt_id_to_query = raw_input("Enter PTT ID you want to query: ")
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
tn.write(ptt_id_to_query + "\r")

#tn.expect([match_str6])
result = tn.read_until(match_str6)
print "match str6"
tn.close()

print result.decode('big5')

ptt_id_info = u"有效文章".encode("big5")
re_result = re.search(ptt_id_info, result)
findall_str = "%s.*\d+.*"%ptt_id_info + u"篇".encode("big5") + ".*"

article_count = -1
split_str1 = " ".encode("big5")
split_str2 = u"》".encode("big5")

if re_result:
    #print "==== yes ===="
    article_count = re.findall(findall_str, result)[0].split(split_str1)[0].\
                        split(split_str2)[1]
else:
    #print "==== no ===="
    pass

try:
    article_count = int(article_count)
except ValueError:
    print "article_count error: %s"%article_count
    exit(-1)
print "article count:",
print article_count
