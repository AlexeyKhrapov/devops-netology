#!/usr/bin/env python3

import socket as s
import time as t
import datetime as dt
import json
import yaml

# set variables
i = 1
count = 1
# check interval in seconds
wait = 2
servers = {'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0', 'google.com': '0.0.0.0'}
init = 0
cfg_path = "/mnt/c/Users/ahr/studing/devops-netology/script/scripts/config_and_log/"
log_file = "/mnt/c/Users/ahr/studing/devops-netology/script/scripts/config_and_log/error.log"

print('*** start script ***')
print(servers)
print('********************')

while True:
    for host in servers:
        ip = s.gethostbyname(host)
        if ip != servers[host]:
            if i == 1 and init != 1:
                is_error = True
                # error output to file
                with open(log_file, 'a') as fl:
                    message = str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' [ERROR] ' + str(host) + ' IP mistmatch: ' + servers[host] + ' ' + ip
                    fl.write(message)
                    print(message)

                    # start of solution for task 2
                    # to different files
                    # json
                    with open(cfg_path + host + ".json", 'w') as jsf:
                        json_data = json.dumps({host: ip})
                        jsf.write(json_data)
                        # yaml
                    with open(cfg_path + host + ".yaml", 'w') as ymf:
                        yaml_data = yaml.dump([{host: ip}])
                        ymf.write(yaml_data)
                        # into a single file
                if is_error:
                    data = []
                    for host in servers:
                        data.append({host: ip})
                    with open(cfg_path + "services_cfg.json", 'w') as jsf:
                        json_data = json.dumps(data)
                        jsf.write(json_data)
                    with open(cfg_path + "services_cfg.yaml", 'w') as ymf:
                        yaml_data = yaml.dump(data)
                        ymf.write(yaml_data)
            servers[host] = ip
    # iteration counter for debugging
    count += 1
    if count >= 20:
        break
    t.sleep(wait)
