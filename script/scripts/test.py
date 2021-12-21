#!/usr/bin/env python3

import os
import sys

path = os.getcwd()
if len(sys.argv)>=2:
    path = sys.argv[1]
bash_command = ["cd "+path, "git status 2>&1"]
print('\033[31m')
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('fatal') != -1:
        print('\033[31m Directory \033[1m '+path+'\033[0m\033[31m is not a GIT repository\033[0m')    
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        prepare_result = prepare_result.replace(' ', '')
        print(prepare_result)
