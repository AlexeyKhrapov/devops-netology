# 4.2. Использование Python для решения типовых DevOps задач — Алексей Храпов

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос  | Ответ                                                                             |
| ------------- |-----------------------------------------------------------------------------------|
| Какое значение будет присвоено переменной `c`?  | значение не может быть присвоено, т.к. переменные разных типов (integer и string) |
| Как получить для переменной `c` значение 12?  | `c = str(a) + b` (преобразовать переменную `a` в строковую)                       |
| Как получить для переменной `c` значение 3?  | `c = a + int(b)` (преобразовать переменную `b` в целочисленную)                   |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?
 
```python
#!/usr/bin/env python3
 
import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/studing/devops-netology", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
#is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
#break
```
 - лишняя логическая переменная `is_change`;
 - команда `breake` прерывает обработку при первом же найденом вхождении.

### Вывод скрипта при запуске при тестировании:
```bash
admin@LP-AHR:/mnt/c/Users/ahr$ ./test.py
.gitignore
script/04-script-01-bash.md
script/04-script-02-py.md
```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
import sys

path = os.getcwd()
if len(sys.argv)>=2:
    path = sys.argv[1]
bash_command = ["cd "+path, "git status 2>&1"]
print('\033[31m')
result_os = os.popen(' && '.join(bash_command)).read()
#is_change = False
for result in result_os.split('\n'):
    if result.find('fatal') != -1:
        print('\033[31m Directory \033[1m '+path+'\033[0m\033[31m is not a GIT repository\033[0m')
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        prepare_result = prepare_result.replace(' ', '')
        print(prepare_result)
#break
```

### Вывод скрипта при запуске при тестировании:
```bash
admin@LP-AHR:/mnt/c/Users/ahr$ ./test.py
 Directory /mnt/c/Users/ahr is not a GIT repository

admin@LP-AHR:/mnt/c/Users/ahr$ ./test.py /mnt/c/Users/ahr/studing/devops-netology/
.gitignore
script/04-script-01-bash.md
script/04-script-02-py.md

admin@LP-AHR:/mnt/c/Users/ahr$ ./test.py ~/devops-netology/
/bin/sh: 1: cd: can't cd to /home/admin/devops-netology/
```
Добавлена обработка наличия параметров:
- при наличии параметра - берется указанный каталог,
- при отсутсвии параметров - берется текущий рабочий каталог,
- при ошибке наличия GIT в каталоге - выдается цветная ошибка.

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
#!/usr/bin/env python3

import socket as s
import time as t
import datetime as dt

# set variables
i = 1
counter = 1
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
  counter += 1
  if counter >= 50:
     break
  t.sleep(wait)
```

### Вывод скрипта при запуске при тестировании:
```bash
admin@LP-AHR:/mnt/c/Users/ahr$ ./test2.py
*** start script ***
{'drive.google.com': '0.0.0.0', 'mail.google.com': '0.0.0.0', 'google.com': '0.0.0.0'}
********************
2021-12-16 17:13:47 [ERROR] drive.google.com IP mistmatch: 0.0.0.0 142.250.74.46
2021-12-16 17:13:47 [ERROR] mail.google.com IP mistmatch: 0.0.0.0 142.250.74.101
2021-12-16 17:13:47 [ERROR] google.com IP mistmatch: 0.0.0.0 142.250.74.142
2021-12-16 17:13:53 [ERROR] drive.google.com IP mistmatch: 142.250.74.46 8.8.8.8
2021-12-16 17:13:53 [ERROR] mail.google.com IP mistmatch: 142.250.74.101 8.8.8.8
2021-12-16 17:13:53 [ERROR] google.com IP mistmatch: 142.250.74.142 8.8.8.8
2021-12-16 17:14:02 [ERROR] drive.google.com IP mistmatch: 8.8.8.8 142.250.74.46
2021-12-16 17:14:02 [ERROR] mail.google.com IP mistmatch: 8.8.8.8 142.250.74.101
2021-12-16 17:14:02 [ERROR] google.com IP mistmatch: 8.8.8.8 142.250.74.142
```

IP-адреса сервисов подменялись путем редактирования файла `hosts`.
Вывод дополнен наличием даты и времени ошибки.