#!/usr/bin/python3
import psutil
import json
from datetime import datetime as dt

result = dict()

now = dt.now()
result['timestamp'] = now.strftime("%s")

#Uptime data (hms format)
def get_uptime_data():
    with open('/proc/uptime', 'r') as log:
        uptime_seconds = int(float(log.read().split(' ')[0].strip()))
    return str(uptime_seconds // 3600) + "h" \
        + str((uptime_seconds % 3600) // 60) + "m" \
        + str(uptime_seconds % 3600 % 60) + "s" 
result['uptime'] = get_uptime_data()


#Running processes
def get_processes_data():
    processes_data = dict()
    with open('/proc/loadavg', 'r') as f:
        for string in f:
            la_1m, la_5m, la_15m, proc_info, newest_pid = string.split(' ')
            running, total = proc_info.split('/')
    processes_data['running'] = int(running)
    processes_data['total'] = int(total)
    return processes_data
result['processes'] = get_processes_data()

#CPU load
result['cpuload_percent'] = psutil.cpu_percent(interval=1)
#Virtual memory load
result['vmload_percent'] = psutil.virtual_memory().percent
#swap lod
result['swapload_percent'] = psutil.swap_memory().percent

#Disks read load
result['disk_io_read'] = psutil.disk_io_counters().read_count
#Disks write load
result['disk_io_write'] = psutil.disk_io_counters().write_count


#Bytes sent
result['net_bytes_sent'] = psutil.net_io_counters().bytes_sent
#Bytes recieved
result['net_bytes_recieved'] = psutil.net_io_counters().bytes_recv

filepath = "/var/log/"+now.strftime("%y-%m-%d")+"-awesome-monitoring.log"

with open(filepath, "a") as log:
    log.write(json.dumps(result)+"\n")