# 5.2. Применение принципов IaaC в работе с виртуальными машинами — Алексей Храпов

## Задача 1

- Опишите своими словами основные преимущества применения на практике IaaC паттернов.
- Какой из принципов IaaC является основополагающим?

### Ответ:

Основополагающий принцип IaaC - описывать инфраструктуру кодом, переиспользуя практики из разработки ПО.
Для его реализации используются основные паттерны:
- `Непрерывная интеграция (CI)`: регулярное объединение изменений программного кода в центральном репозитории, после чего автоматически выполняется сборка, тестирование и запуск. Позволяет быстрее находить и исправлять ошибки и противоречия, за счет чего улучшать качество ПО и сокращать временные и трудовые затраты на проверку и выпуск новых обновлений ПО. Как итог снижается стоимость исправление дефекта.


- `Непрерывная доставка (CD)`: автоматическая сборка, тестирование и подготовка к окончательному выпуску при любых изменениях в программном коде (все изменения кода после стадии сборки развертываются в тестовой и/или в рабочей среде). Позволяет не только автоматизировать тестирование на уровне модулей, но и выполнять разноплановую проверку обновлений приложений перед тем, как развертывать их для конечных пользователей. Иными словами позволяет тщательнее проверять обновления и заблаговременно выявлять возможные проблемы. Как итог качество кода повышается, а трудозатраты на его обеспечение снижаются. Требует ручного запуска.


- `Непрерывное развёртывание (CD)`: упраздняет ручные действия в непрерывной доставке. Обычно применяется на тестовой среде (в релиз развёртывание предпочтительнее отправлять вручную).


---
## Задача 2

- Чем Ansible выгодно отличается от других систем управление конфигурациями?
- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?
### Ответ:
Выгодное отличие Ansible от других систем - не требуется установки агентов на управляемые узлы, все функции производятся с использованием существующей инфраструктуры SSH

На мой взгляд, системы конфигурации, использующие метод push, более надежны, т.к. все конфигурации хранятся локально в том виде, в котором удобно администратору, следовательно, не возникнет простоя в работе и сбоев при распространении конфигурации, если возникнут неполадки на сервере, хранящем конфигурации. Такие серверы используются системами, использующие метод pull. 

---
## Задача 3

Установить на личный компьютер:

- VirtualBox
- Vagrant
- Ansible

*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*
### Ответ:
```bash
alex@NewMonitoring:~$ vagrant -v
Vagrant 2.2.19
alex@NewMonitoring:~$ vboxmanage --version
6.1.32r149290
alex@NewMonitoring:~$ ansible --version
ansible 2.9.6
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/alex/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Nov 26 2021, 20:14:08) [GCC 9.3.0]
```
---
## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

- Создать виртуальную машину.
- Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды
```
docker ps
```
### Ответ:
```bash
alex@NewMonitoring:~/src/vagrant$ vagrant up
Bringing machine 'server1.netology' up with 'virtualbox' provider...
==> server1.netology: Importing base box 'bento/ubuntu-20.04'...
==> server1.netology: Matching MAC address for NAT networking...
==> server1.netology: Checking if box 'bento/ubuntu-20.04' version '202107.28.0' is up to date...
==> server1.netology: Setting the name of the VM: server1.netology
==> server1.netology: Clearing any previously set network interfaces...
==> server1.netology: Preparing network interfaces based on configuration...
    server1.netology: Adapter 1: nat
    server1.netology: Adapter 2: hostonly
==> server1.netology: Forwarding ports...
    server1.netology: 22 (guest) => 20011 (host) (adapter 1)
    server1.netology: 22 (guest) => 2222 (host) (adapter 1)
    server1.netology: 22 (guest) => 2222 (host) (adapter 1)
==> server1.netology: Running 'pre-boot' VM customizations...
==> server1.netology: Booting VM...
==> server1.netology: Waiting for machine to boot. This may take a few minutes...
    server1.netology: SSH address: 172.30.96.1:2222
    server1.netology: SSH username: vagrant
    server1.netology: SSH auth method: private key
    server1.netology: Warning: Connection reset. Retrying...
    server1.netology:
    server1.netology: Vagrant insecure key detected. Vagrant will automatically replace
    server1.netology: this with a newly generated keypair for better security.
    server1.netology:
    server1.netology: Inserting generated public key within guest...
    server1.netology: Removing insecure key from the guest if it's present...
    server1.netology: Key inserted! Disconnecting and reconnecting using new SSH key...
==> server1.netology: Machine booted and ready!
==> server1.netology: Checking for guest additions in VM...
==> server1.netology: Setting hostname...
==> server1.netology: Configuring and enabling network interfaces...
==> server1.netology: Running provisioner: ansible...
    server1.netology: Running ansible-playbook...
[WARNING]: Ansible is being run in a world writable directory
(/home/alex/src/vagrant), ignoring it as an ansible.cfg source. For more
information see
https://docs.ansible.com/ansible/devel/reference_appendices/config.html#cfg-in-
world-writable-dir

PLAY [nodes] *******************************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1.netology]

TASK [Create directory for ssh-keys] *******************************************
changed: [server1.netology]

TASK [Adding rsa-key in /root/.ssh/authorized_keys] ****************************
changed: [server1.netology]

TASK [Checking DNS] ************************************************************
changed: [server1.netology]

TASK [Installing tools] ********************************************************
[DEPRECATION WARNING]: Invoking "apt" only once while using a loop via
squash_actions is deprecated. Instead of using a loop to supply multiple items
and specifying `package: "{{ item }}"`, please use `package: ['git', 'curl']`
and remove the loop. This feature will be removed in version 2.11. Deprecation
warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [server1.netology] => (item=['git', 'curl'])

TASK [Installing docker] *******************************************************
[WARNING]: Consider using the get_url or uri module rather than running 'curl'.
If you need to use command because get_url or uri is insufficient you can add
'warn: false' to this command task or set 'command_warnings=False' in
ansible.cfg to get rid of this message.
changed: [server1.netology]

TASK [Add the current user to docker group] ************************************
changed: [server1.netology]

PLAY RECAP *********************************************************************
server1.netology           : ok=7    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

alex@NewMonitoring:~/src/vagrant$ vagrant ssh
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sun 23 Jan 2022 07:22:45 PM UTC

  System load:  0.22              Users logged in:          0
  Usage of /:   3.2% of 61.31GB   IPv4 address for docker0: 172.17.0.1
  Memory usage: 20%               IPv4 address for eth0:    10.0.2.15
  Swap usage:   0%                IPv4 address for eth1:    192.168.56.11
  Processes:    110


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Sun Jan 23 19:20:43 2022 from 10.0.2.2
vagrant@server1:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```