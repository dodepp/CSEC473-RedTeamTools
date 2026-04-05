import random
import threading
import time

SMB_SERVER_IP = ""

def smb_flood_work(target_host):
    while True:
        time.sleep(random.randrange(5)/1000)

def smb_flood(target_host):
    t = threading.Thread(target=smb_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    dns_thread = smb_flood(SMB_SERVER_IP)

if __name__ == "__main__":
    main()