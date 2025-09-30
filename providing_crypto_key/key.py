from cryptography.fernet import Fernet
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
key = Fernet.generate_key()

with open(os.path.join(BASE_DIR, "secret_key_2.txt"), mode = "wb") as sec_file:
    sec_file.write(key)
