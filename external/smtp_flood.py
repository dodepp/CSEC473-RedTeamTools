import random
import threading
import time

SMTP_SERVER_IP = ""

def smtp_flood_work(target_host):
    while True:
        time.sleep(random.randrange(5)/1000)

def smtp_flood(target_host):
    t = threading.Thread(target=smtp_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    dns_thread = smtp_flood(SMTP_SERVER_IP)

if __name__ == "__main__":
    main()