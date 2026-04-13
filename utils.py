import random
import string

DOMAIN_CONTROLLER_IP = "10.10.10.21"
SMB_SERVER_IP = "10.10.10.22"
SMTP_SERVER_IP = "10.10.10.23"
WINDOWS_TARGET_IPS = [DOMAIN_CONTROLLER_IP, SMB_SERVER_IP, SMTP_SERVER_IP]

APACHE_SERVER_IP = "10.10.10.101"
MYSQL_SERVER_IP = "10.10.10.102"
SSH_SERVER_IP = "10.10.10.103"
OPENVPN_SERVER_IP = "10.10.10.104"
LINUX_TARGET_IPS = [APACHE_SERVER_IP, MYSQL_SERVER_IP, SSH_SERVER_IP, OPENVPN_SERVER_IP]


usernames = ["admin", "root"]
passwords = ["password", "12345", "root", "toor", "admin", "snake"]

def random_ip():
    d = random.choice(list(range(1, 200)) + list(range(211, 254)))
    return f"10.10.10.{d}"

def random_string(length=12):
    characters = string.ascii_letters + string.digits
    rand_str = ''.join(random.choices(characters, k=length))
    return rand_str