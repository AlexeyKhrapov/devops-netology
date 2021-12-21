#!/usr/bin/env python3

import socket as s
import time as t
import datetime as dt

# set variables
i = 1
count = 1
# check interval in seconds
wait = 2
servers = {'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0', 'google.com': '0.0.0.0'}
init = 0

print('*** start script ***')
print(servers)
print('********************')


while 1 == 1: # debug number of checks
  for host in servers:
    ip = s.gethostbyname(host)
    if ip != servers[host]:
      if i == 1 and init != 1:
        print(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +' [ERROR] ' + str(host) +' IP mistmatch: '+servers[host]+' '+ip)
      servers[host] = ip

# iteration counter for debugging
  count += 1
  if count >= 50:
     break
  t.sleep(wait)

