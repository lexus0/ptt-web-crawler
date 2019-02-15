# -*- coding: big5 -*-

import re

with open("ptt_id_info.txt", "r") as f:
    result = f.read()

result_big5 = result.decode("big5")
print result_big5
ptt_id_info = u"有效文章".encode("big5")
re_result = re.search(ptt_id_info, result)
#sub_str = ".*%s.*(\d+).*篇.*"%ptt_id_info
findall_str = "%s.*\d+.*篇.*"%ptt_id_info

article_count = -1
split_str1 = " ".encode("big5")
split_str2 = "》"

if re_result:
    print "==== yes ===="
    #article_count = re.sub(sub_str, "\g<1>", result)
    article_count = re.findall(findall_str, result)[0].split(split_str1)[0].\
                        split(split_str2)[1]
else:
    print "==== no ===="

try:
    article_count = int(article_count)
except ValueError:
    print "article_count error: %s"%article_count
    exit(-1)
print "article count:",
print article_count
