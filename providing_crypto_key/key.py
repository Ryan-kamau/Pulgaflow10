from cryptography.fernet import Fernet

key = Fernet.generate_key()

with open("secret_key_2.txt", mode = "wb") as sec_file:
    sec_file.write(key)
