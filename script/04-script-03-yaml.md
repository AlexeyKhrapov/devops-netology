# 4.3. Языки разметки JSON и YAML — Алексей Храпов


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис.

### Ответ:
 - не хватает запятой между значениями массива (6 строка);
 - не хватает кавычек (9 строка).

Исправленный вариант:
```json
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
```

## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
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

```

### Вывод скрипта при запуске при тестировании:
```
admin@LP-AHR:/mnt/c/Users/ahr/studing/devops-netology/script/scripts$ ./04-03_2.py
*** start script ***
{'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0', 'google.com': '0.0.0.0'}
********************
2021-12-21 21:51:50 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:51:50 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:51:50 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:51:52 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:51:52 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:51:52 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:51:54 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:51:54 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:51:54 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:51:56 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:51:56 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:51:56 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:51:58 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:51:58 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:51:58 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:00 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:00 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:00 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:02 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:02 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:02 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:04 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:04 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:04 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:06 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:06 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:06 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:08 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:08 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:08 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:10 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:10 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:10 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:12 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:12 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:12 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:14 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:15 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:15 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:17 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:17 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:17 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:19 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:19 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:19 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:21 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:21 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:21 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:23 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:23 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:23 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:25 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:25 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:25 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
2021-12-21 21:52:27 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 209.85.233.194
2021-12-21 21:52:27 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 216.58.210.133
2021-12-21 21:52:27 [ERROR] google.com IP mistmatch: 216.58.210.133 216.58.210.142
```

### json-файл(ы), который(е) записал ваш скрипт:
```json
{"drive.google.com": "209.85.233.194"}
```
```json
{"google.com": "216.58.210.142"}
```
```json
{"mail.google.com": "216.58.210.133"}
```
```json
[{"drive.google.com": "216.58.210.142"}, {"mail.google.com": "216.58.210.142"}, {"google.com": "216.58.210.142"}]
```
### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
- drive.google.com: 209.85.233.194
```
```yaml
- google.com: 216.58.210.142
```
```yaml
- mail.google.com: 216.58.210.133
```
```yaml
- drive.google.com: 216.58.210.142
- mail.google.com: 216.58.210.142
- google.com: 216.58.210.142
```