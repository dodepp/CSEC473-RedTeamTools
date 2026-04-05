import random
import threading
import time

APACHE_SERVER_IP = ""

def apache_flood_work(target_host):
    while True:
        time.sleep(random.randrange(5)/1000)

def apache_flood(target_host):
    t = threading.Thread(target=apache_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    dns_thread = apache_flood(APACHE_SERVER_IP)

if __name__ == "__main__":
    main()