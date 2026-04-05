import random
import string

def random_ip():
    c = random.randint(1, 254)
    d = random.randint(1, 254)
    return "10.10." + str(c) + "." + str(d)

def random_string(length=12):
    characters = string.ascii_letters + string.digits
    rand_str = ''.join(random.choices(characters, k=length))
    return rand_str