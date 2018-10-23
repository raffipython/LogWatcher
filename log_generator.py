#!/usr/bin/python

""" Not written by me:
    Heavy modified version of https://github.com/kiritbasu/Fake-Apache-Log-Generator"""

import time
import datetime
import random
import sys
import argparse

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

parser = argparse.ArgumentParser(__file__, description="Fake Apache Log Generator")
parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int, default=1)
parser.add_argument("--sleep", "-s", help="Sleep this long between lines (in seconds)", default=0.0, type=float)

args = parser.parse_args()

log_lines = args.num_lines


timestr = time.strftime("%Y%m%d-%H%M%S")
otime = datetime.datetime.now()

f = sys.stdout

response=["200","404","500","301"]
verb=["GET","POST","DELETE","PUT"]
resources=["/list","/wp-content.png","/wp-admin.png"]

ualist = ["test uasdf us "]

flag = True
while (flag):
    if args.sleep:
        increment = datetime.timedelta(seconds=args.sleep)
    else:
        increment = datetime.timedelta(seconds=random.randint(30, 300))
    otime += increment

    ip_list = ["1.1.1.1", "2.100.15.1", "255.255.255.255", "123.41.4.111", "10.10.1.1"]
    ip = random.choice(ip_list)
    dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now().strftime('%z')
    vrb = "2"

    uri = random.choice(resources)
    if uri.find("apps")>0:
        uri += str(random.randint(1000,10000))

    code = ["GET", "POST","GTFO"]
    resp = random.choice(code) #"5000"

    idz = ["ABCD", "AZYR", "NOEN", "YAYE", "TEST"]
    ids = random.choice(idz)

    byt = int(random.gauss(5000,50))

    referer = "/whynot.png " #aker.uri()
    #print "127.0.0.1 - ABCD [22/Oct/2018:12:38:12 -0700] \"GET /sample-image.png HTTP/2\" 200 1479"
    f.write("{} - {} [{} -0000] \"{} {}\n".format(ip, ids, dt, resp, uri))
    f.flush()

    log_lines = log_lines - 1
    flag = False if log_lines == 0 else True
    if args.sleep:
        time.sleep(args.sleep)
