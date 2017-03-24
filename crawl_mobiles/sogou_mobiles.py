#!/usr/bin/env python
# coding=utf-8

import requests
import logging
import random
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.INFO, filename="sogou_mobiles.log", filemode = 'w')

sess = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
sess.get('https://www.sogou.com', headers=headers)
ips = [("*.*.*.0", "3128"), ("*.*.*.1", "3128")]
url = 'https://www.sogou.com/websearch/phoneAddress.jsp'

def queryMobile(mobile):
    ind = random.randint(0, len(ips)-1)
    proxies = { "http": "http://"+ ips[ind][0] + ":" + ips[ind][1] }
    params = {'phoneNumber': mobile, 'cb': 'handlenumber'}
    
    response = sess.get(url, proxies=proxies, params=params)
    if (not response.ok):
        logging.info("can't query: %s" % mobile)
        return None
    resmsg = re.search('\"(.+?)\"', response.text)
    if resmsg is None:
       logging.info("%s is null" % mobile)
       return None
    data = resmsg.group(1).split()
    addr = data[0]
    citycode = ''
    card = data[1]
    return "%s,%s,%s,%s" % (mobile, addr, citycode, card)


s_id = [134,135,136,137,138,139,147,150,151,152,157,158,159,178,182,183,184,187,188,130,131,132,145,155,156,171,175,176,185,186,133,149,153,173,177,180,181,189,170]
#s_m = [ s.zfill(4) for s in list(map(str, range(10000)))]
with open('mobiles.csv', 'w') as outfile:
    for op in s_id:
        for m in range(10000):
            mobile = str(op) + str(m).zfill(4) + str(random.randint(1000, 9999))
            print("query " + mobile)
            result = queryMobile(mobile)
            if result is not None:
                outfile.write("%s,%s\n"%(op,result))

print("done")

