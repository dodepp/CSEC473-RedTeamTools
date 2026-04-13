'''
5 timers:
- cups-clean.timer: 5 mins
- dbus-sync.timer: 30 sec
- getty.timer: 1 min
- syslog-refresh.timer: 1 min
- firewalld.timer: 2 mins
'''
import os
import subprocess

CUPS_TIMER = {"name": "cups-clean", "time": "5m", "exec":"/usr/sbin/cupsd -t", "timer_description":"Triggers the CUPS Cleaner every 5 minutes", "service_description":"Cleans out old CUPS print jobs"}
DBUS_TIMER = {"name": "dbus-sync", "time": "30s", "exec":"/usr/bin/busctl list -l", "timer_description":"Triggers DBUS synchronization every 30 seconds", "service_description":"Synchronizes DBUS for important processes"}
GETTY_TIMER = {"name": "getty", "time": "1m", "exec":"/usr/sbin/getty --list-speeds", "timer_description":"Triggers getty service commands every minute", "service_description":"Service commands to keep getty functional"}
SYSLOG_TIMER = {"name": "syslog-refresh", "time": "1m", "exec":"/usr/bin/logger \"refresh\"", "timer_description":"Triggers a refresh of syslog every minute", "service_description":"Refreshes the syslog utility"}
FIREWALL_TIMER = {"name": "firewalld", "time": "2m", "exec":"/usr/bin/firewall-cmd --reload", "timer_description":"Triggers a configuration check of firewalld every 2 minutes", "service_description":"Checks for valid configuration of firewalld"}

TIMERS = [CUPS_TIMER, DBUS_TIMER, GETTY_TIMER, SYSLOG_TIMER, FIREWALL_TIMER]

TIMER_PATH = "/etc/systemd/system"

def create_timer_file(timer):
    timer_content = f"""
    [Unit]
    Description={timer["timer_description"]}

    [Timer]
    OnBootSec={timer["time"]}
    OnUnitActiveSec={timer["time"]}

    [Install]
    WantedBy=timers.target
    """
    return timer_content

def create_service_file(timer):
    service_content = f"""
    [Unit]
    Description={timer["service_description"]}
    After=network.target

    [Service]
    ExecStart={timer["exec"]}
    Type=oneshot
    User=root
    """
    return service_content

def implant_timer(timer):
    t_abs_filename = os.path.join(TIMER_PATH, timer["name"] + ".timer")
    s_abs_filename = os.path.join(TIMER_PATH, timer["name"] + ".service")
    with open(t_abs_filename, "w") as f:
        f.write(create_timer_file(timer))
    with open(s_abs_filename, "w") as f:
        f.write(create_service_file(timer))
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "--now", f"{timer["name"]}.timer"])

def main():
    if os.geteuid() != 0:
        print("This script requires root privileges. Please run with: sudo python3 timer_noise.py")
        return

    for timer in TIMERS:
        implant_timer(timer)
        print(f"Timer \"{timer["name"]}\" implanted")
    print("Done.")

    

if __name__ == "__main__":
    main()