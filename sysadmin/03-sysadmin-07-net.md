# 3.7. Компьютерные сети, лекция 2 — Алексей Храпов

> 1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?

Windows(`ipconfig`, `netsh interface show interface`):
```cmd
PS C:\Users\ahr> ipconfig

Настройка протокола IP для Windows


Адаптер Ethernet Ethernet 2:

   Состояние среды. . . . . . . . : Среда передачи недоступна.
   DNS-суффикс подключения . . . . . :

Адаптер Ethernet vEthernet (Default Switch):

   DNS-суффикс подключения . . . . . :
   IPv4-адрес. . . . . . . . . . . . : 172.22.224.1
   Маска подсети . . . . . . . . . . : 255.255.240.0
   Основной шлюз. . . . . . . . . :

Адаптер Ethernet vEthernet (Беспроводная се):

   DNS-суффикс подключения . . . . . :
   IPv4-адрес. . . . . . . . . . . . : 172.28.192.1
   Маска подсети . . . . . . . . . . : 255.255.240.0
   Основной шлюз. . . . . . . . . :

Адаптер Ethernet vEthernet (WSL):

   DNS-суффикс подключения . . . . . :
   IPv4-адрес. . . . . . . . . . . . : 172.23.96.1
   Маска подсети . . . . . . . . . . : 255.255.240.0
   Основной шлюз. . . . . . . . . :

Адаптер беспроводной локальной сети Подключение по локальной сети* 1:

   Состояние среды. . . . . . . . : Среда передачи недоступна.
   DNS-суффикс подключения . . . . . :

Адаптер беспроводной локальной сети Подключение по локальной сети* 2:

   Состояние среды. . . . . . . . : Среда передачи недоступна.
   DNS-суффикс подключения . . . . . :

Адаптер беспроводной локальной сети Беспроводная сеть:

   DNS-суффикс подключения . . . . . : sofp.local
   IPv4-адрес. . . . . . . . . . . . : 172.18.213.3
   Маска подсети . . . . . . . . . . : 255.255.255.0
   Основной шлюз. . . . . . . . . : 172.18.213.1

Адаптер Ethernet Сетевое подключение Bluetooth:

   Состояние среды. . . . . . . . : Среда передачи недоступна.
   DNS-суффикс подключения . . . . . :

Адаптер Ethernet vEthernet (Ethernet 2):

   DNS-суффикс подключения . . . . . :
   IPv4-адрес. . . . . . . . . . . . : 172.29.240.1
   Маска подсети . . . . . . . . . . : 255.255.240.0
   Основной шлюз. . . . . . . . . :
PS C:\Users\ahr> netsh interface show interface

Состояние адм.  Состояние     Тип              Имя интерфейса
---------------------------------------------------------------------
Разрешен       Подключен      Выделенный       Беспроводная сеть
Разрешен       Отключен       Выделенный       Ethernet 2
Разрешен       Подключен      Выделенный       vEthernet (Ethernet 2)
Разрешен       Подключен      Выделенный       vEthernet (Default Switch)
Разрешен       Подключен      Выделенный       vEthernet (Беспроводная се)
Разрешен       Подключен      Выделенный       vEthernet (WSL)
```
Linux (`ip link`, `ifconfig -a`):
```bash
admin@LP-AHR:/mnt/c/Users/ahr$ ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: bond0: <BROADCAST,MULTICAST,MASTER> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 8a:84:0f:80:8a:f0 brd ff:ff:ff:ff:ff:ff
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether fe:dd:91:ff:82:a3 brd ff:ff:ff:ff:ff:ff
4: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:15:5d:7e:27:7a brd ff:ff:ff:ff:ff:ff
5: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ipip 0.0.0.0 brd 0.0.0.0
6: sit0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN mode DEFAULT group default qlen 1000
admin@LP-AHR:/mnt/c/Users/ahr$ ifconfig -a
bond0: flags=5122<BROADCAST,MASTER,MULTICAST>  mtu 1500
        ether 8a:84:0f:80:8a:f0  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

dummy0: flags=130<BROADCAST,NOARP>  mtu 1500
        ether fe:dd:91:ff:82:a3  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.23.100.151  netmask 255.255.240.0  broadcast 172.23.111.255
        inet6 fe80::215:5dff:fe7e:277a  prefixlen 64  scopeid 0x20<link>
        ether 00:15:5d:7e:27:7a  txqueuelen 1000  (Ethernet)
        RX packets 28733  bytes 94319423 (89.9 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 7162  bytes 513344 (501.3 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

sit0: flags=128<NOARP>  mtu 1480
        sit  txqueuelen 1000  (IPv6-in-IPv4)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tunl0: flags=128<NOARP>  mtu 1480
        tunnel   txqueuelen 1000  (IPIP Tunnel)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
> 2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?

Протокол: `LLDP`

Пакет: `lldpd`
> 3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.

Технология: `VLAN`

Пакет: `vlan`

Команды (пример из man, который инкапсулирует входящие пакеты ICMP на eth0 из 10.0.0.2 в VLAN ID 123)
```bash
tc qdisc add dev eth0 handle ffff: ingress
tc filter add dev eth0 parent ffff: pref 11 protocol ip \
u32 match ip protocol 1 0xff flowid 1:1 \
match ip src 10.0.0.2 flowid 1:1 \
action vlan push id 123
```

Пример конфигурации vlan с бриджом на 2 интерфейса:
```bash
# VLAN3
auto enp65s0f0.3
iface enp65s0f0.3 inet manual
    vlan-raw-device enp65s0f0

auto enp65s0f1.3
iface enp65s0f1.3 inet manual
    vlan-raw-device enp65s0f1

auto vmbr3
iface vmbr3 inet manual
    bridge_ports enp65s0f0.3 enp65s0f1.3
    bridge_stp off
    bridge_fd 0
    # VLAN3
```
> 4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.

Типы агрегации интерфейсов в Linux:
- статическая
- динамическая

Опции:

- 0 - `balance-rr` - (round-robin) - режим циклического выбора активного интерфейса для исходящего трафика (рекомендован для включения по умолчанию, не требует применения специальных коммутаторов);
- 1 - `active-backup` - активен только один интерфейс, остальные в режиме горячей замены (самый простой режим, работает с любым оборудованием, не требует применения специальных коммутаторов);
- 2 - `balance-xor` - режим, в котором каждый получатель закрепляется за одним из физических интерфейсов, который выбирается по специальной формуле (не требует применения специальных коммутаторов);
- 3 - `broadcast` - трафик идет через все интерфейсы одновременно (примитивный и потенциально конфликтный режим);
- 4 - `802.3ad` - (dynamic link aggregation) - в группу объединяются одинаковые по скорости и режиму интерфейсы. Все физические интерфейсы используются одновременно в соответствии со спецификацией IEEE 802.3ad. Для реализации этого режима необходима поддержка на уровне драйверов сетевых карт и коммутатор, поддерживающий стандарт IEEE 802.3ad (коммутатор требует отдельной настройки);
- 5 - `balance-tlb` - (adaptive transmit load balancing) - исходящий трафик распределяется в соответствии с текущей нагрузкой (с учетом скорости) на интерфейсах (для данного режима необходима его поддержка в драйверах сетевых карт);
- 6 - `balance-alb` - (adaptive load balancing) - включает в себя balance-tlb, плюс балансировку на приём (rlb) для IPv4 трафика и не требует применения специальных коммутаторов (балансировка на приём достигается на уровне протокола ARP, перехватом ARP ответов локальной системы и перезаписью физического адреса на адрес одного из сетевых интерфейсов, в зависимости от загрузки).

Пример:
```bash
auto eth0
iface eth0 inet manual
    bond-master bond0
    bond-primary eth0
    bond-mode active-backup
   
auto wlan0
iface wlan0 inet manual
    wpa-conf /etc/network/wpa.conf
    bond-master bond0
    bond-primary eth0
    bond-mode active-backup

# Define master
auto bond0
iface bond0 inet dhcp
    bond-slaves none
    bond-primary eth0
    bond-mode active-backup
    bond-miimon 100
```
> 5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.

Максимальн возможное количество IP-адресов в сети с маской /29: `8` (но колчисество хостов ограничивается шестью)

Максимально возможное количество подсетей /29 в сети с маской /24: `32`

> 6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.

Частные адреса допустимо взять из `100.64.0.0/10` (Carrier-Grade NAT).
Исходя из поставленной задачи, подсеть будет `100.64.0.0/26`, даже небольшой запас останется (но маски /27 уже не хватит).

> 7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?

Для проверки и в Windows, и в Linux: `arp -a`, в современных версиях Linux можно использовать `ip neigh`.

Для полной очистки ARP кеша:

- В Windows `netsh interface ip delete arpcache`
- В Linux `ip neigh flush all` (требуются права суперпользователя)

Для удаления конкретного адреса (для примера 192.168.2.54): `arp -d 192.168.2.54`, в современных версиях Linux можно использовать для интерфейса eth0 `ip neigh del 192.168.2.54 dev eth0`