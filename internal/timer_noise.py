'''
5 timers:
- cups-clean.timer: 5 mins
- dbus-sync.timer: 30 sec
- getty.timer: 1 min
- syslog-refresh.timer: 1 min
- firewalld.timer: 2 mins
'''
import os

CUPS_TIMER = {"name": "cups-clean", "time": "", }
DBUS_TIMER = {"name": "dbus-sync", "time": ""}
GETTY_TIMER = {"name": "getty"}
SYSLOG_TIMER = {"name": "syslog-refresh"}
FIREWALL_TIMER = {"name": "firewalld"}

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
    ExecStart=
    Type=oneshot
    User=root
    """
    return service_content

def implant_timer(timer):
    ...


def main():
    for timer in TIMERS:
        implant_timer(timer)
        print(f"Timer \"{timer["name"]}\" created")

    

if __name__ == "__main__":
    main()