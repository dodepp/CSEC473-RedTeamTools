import random
import threading
import time

MYSQL_SERVER_IP = ""

def mysql_flood_work(target_host):
    while True:
        time.sleep(random.randrange(5)/1000)

def mysql_flood(target_host):
    t = threading.Thread(target=mysql_flood_work, args=(target_host,), daemon=True)
    t.start()
    return t

def main():
    dns_thread = mysql_flood(MYSQL_SERVER_IP)

if __name__ == "__main__":
    main()