首先声明,github抄的，改了一点点内容

使用方法： python cfscan.py 183.201.1.1-183.201.255.255 800

cfscan.py = 你保存的文件名

183.201.1.1-183.201.255.255 = 你要扫的起始IP-结尾IP

800 = 线程数


脚本代码：

#!/usr/bin/env python
# coding=utf-8
# python2.7 only

import threading
import requests
import Queue
import sys
import re

#ip to num
def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

#num to ip
def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,(num & 0x00ff0000) >> 16,(num & 0x0000ff00) >> 8,num & 0x000000ff)

#
def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]

#
def bThread(iplist):
    
    threadl = []
    queue = Queue.Queue()
    for host in iplist:
        queue.put(host)

    for x in xrange(0, int(SETTHREAD)):
        threadl.append(tThread(queue))
        
    for t in threadl:
        t.start()
    for t in threadl:
        t.join()        

#create thread
class tThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        
        while not self.queue.empty(): 
            host = self.queue.get()
            try:
                checkServer(host)
            except:
                continue

def checkServer(host):
    header ={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
    aimurl = "http://"+host+":443"
    response = requests.get(url=aimurl,headers=header,timeout=10)
    serverText = response.headers['server']

    if len(serverText) > 0:
        print  "-"*50+"\n"+aimurl +"\nServer: "+serverText
        if (serverText == "CloudFront"):
            f.write(host+"\n")


if __name__ == '__main__':
    print '\n############# Cloud Front Scan  ################'
    print '                Author hostloc.com'
    print '################################################\n'

    global SETTHREAD

    try:
        SETTHREAD = sys.argv[2]
        f = open("result.txt", "w")
        iplist = ip_range(sys.argv[1].split('-')[0], sys.argv[1].split('-')[1])
        
        print '\n[Note] Will scan '+str(len(iplist))+" host...\n"

        bThread(iplist)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt!'
        sys.exit()
