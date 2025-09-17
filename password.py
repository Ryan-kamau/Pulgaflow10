from cryptography.fernet import Fernet




def main():
    # Load the encryption key from file
    key = load_key()

    # Load account details from file (decrypting them)
    details = load_file("passwords.txt", key)
    while True:
         print("\nWHAT OPERATION DO YOU WANNA DO: \n1 - DISPLAY DETAILS \n2 - ADD ACCOUNT DETAILS \n3 - UPDATE ACCOUNT DETAILS \n4 - DELETE ACCOUNT \n5 - SAVE TO A FILE \n6 - exit")
         try:
            # Prompt user for operation choice
            operation = int(input("\t\tWHAT DO YOU CHOOSE? "))
         except ValueError:
             print("INVALID INPUT.... THAT IS NOT AN INTEGER..... TRY AGAIN")
             continue
         
         # Match user choice to operation
         match operation:
             case 1:
                 display_details(details)
             case 2:
                 add_account(details, "passwords.txt", key)
             case 3:
                 update_details(details, "passwords.txt", key)
             case 4:
                 delete_accounts(key, "passwords.txt", details)
             case 5:
                 save_file("passwords.txt", details, key)
             case 6:
                 break
             case _:
                 print("not an option")
    pass 

# Load account details from file, decrypting them with the key
# If file not found, return default details

def load_file(filename, key):
    try:
        details = []
        with open(filename, mode ="r") as file:
            for accounts in file:
                # Split each line into account, username, and password
                jina, usern, passc = [value.strip() for value in accounts.strip().split(',')]
                # Decrypt each field using Fernet
                dename = de_crypt(jina, key)
                deuser = de_crypt(usern, key)
                depass = de_crypt(passc, key)
                dis1 = {"account":dename, "username":deuser, "password":depass} 
                details.append(dis1)
        print("\n\t\tLOADED ALL DETAILS FROM FILE")
    except FileNotFoundError:
        # If file not found, use default details
        print("\n File not found printing OG details\n")    
        details = [
            {"account":"Email", "username":"ryankamau@gmail.com", "password":"LETsgo"},
            {"account":"Youtube", "username":"ryan", "password":"Whatdidimiss"}
        ]
    
    return details

# Add new account details to the list, then save them (encrypted)
# Prompts user for number of accounts and their details

def add_account(details, filename, key):
    while True:  
        try:
            ongeza = int(input("\n How many Account details do you want to add? "))
            break
        except ValueError:
            print("That's Not An integer. Try Again\n")
        
    for i in range(ongeza):
        print(f"\t\taccount {i+1}")
        # Prompt for new account details
        jina = input("Account: ").title()
        user = input("Username: ")
        psw = input("Password: ")
        print("\n")
        new_det = {"account":jina, "username":user, "password":psw}
        details.append(new_det)
        

    # Print all account details after addition
    print("\n     PRINTING ALL ACC DETAILS")
    for i, accounts in enumerate(details, start = 1):
        print(f"\t{i}. {accounts['account']} ACCOUNT => USERNAME is {accounts['username']} => PASSWORD is {accounts['password']}")    
    # Save the updated details to file (encrypted)
    save_file("passwords.txt", details, key)

    return details

# Display all account detailss

def display_details(details):
    # Print all loaded or default details
    print("\n Printing OG details\n")
    for i, accounts in enumerate(details, start = 1):
        print(f"\t\t{i}. {accounts['account']} ACCOUNT => USERNAME is {accounts['username']} => PASSWORD is {accounts['password']}")
# Save account details to file, encrypting them with the key

def save_file(filename, details, key):
    # Encrypt all account details while saving
    Edetails = []
    for accounts in details:
        crypt1, crypt2, crypt3 = accounts['account'], accounts['username'], accounts['password']
        encrypt1, encrypt2, encrypt3 = encrypt(crypt1, key), encrypt(crypt2, key), encrypt(crypt3, key)
        enc_accounts =  {"account":encrypt1, "username":encrypt2, "password":encrypt3}
        Edetails.append(enc_accounts)
    with open(filename, mode = "w") as file:
        for accounts in Edetails:
            file.write(f"{accounts['account']}, {accounts['username']}, {accounts['password']}\n")
    print("\t\tSAVED TO FILE")
    

# Fernet encryption for a single string
# crypt_word: the string to encrypt
# key: the Fernet key (bytes)
def encrypt(crypt_word, key):
    f = Fernet(key)
    encrypted = f.encrypt(crypt_word.encode())
    return encrypted.decode()  # Return as string for storage

# Fernet decryption for a single string
# enc_words: the string to decrypt
# key: the Fernet key (bytes)
def de_crypt(enc_words, key):
    f = Fernet(key)
    decrypt = f.decrypt(enc_words.encode())
    return decrypt.decode()  # Return as string for use

# Update existing account details, then save them (encrypted)
# Prompts user for how many accounts to update, which account, and which field
def update_details(details, filename, key):
    print("\t\t UPDATING .....")
    while True:
        try:
            upddet = int(input("How many accounts do you want to update? "))
            if upddet > len(details):
                raise IndexError(f"\tCANNOT DO OPERATION THAT NUMBER OF TIMES...ONLY {len(details)} present")
            break
        except ValueError:
            print("INVALID INPUT...TRY AGAIN")
        except IndexError as e:
            print(e)
    for i in range(upddet):
        print("\n Printing Details\n")
        for i, accounts in enumerate(details, start = 1):
             print(f"\t\t{i}. {accounts['account']} ACCOUNT => USERNAME is {accounts['username']} => PASSWORD is {accounts['password']}")        # Get valid account selection
        while True:
            try:
                selection = int(input("Account number you want to change from the details: ")) - 1
                if selection < 0 or selection >= len(details):
                    print(f"Please enter a number between 1 and {len(details)}.")
                    continue
                break
            except ValueError:
                print("INVALID INPUT...TRY AGAIN")
        # Get valid field choice
        while True:
            try:
                choice = int(input("DO you want to change \n1 - Username \n2 - Password \n PICK AN OPTION: "))
                if choice not in [1, 2]:
                    print("NOT AN OPTION")
                    continue
                break
            except ValueError:
                print("INVALID INPUT...TRY AGAIN")
        match choice:
            case 1:
                details[selection]['username'] = input("NEW USERNAME:  ")
            case 2:
                details[selection]['password'] = input("NEW PASSWORD:  ")

    # Save the updated details to file (encrypted)
    save_file("passwords.txt", details, key)
    return details

# Load the Fernet key from file
# Returns the key as bytes
def load_key():
    with open("secret_key.txt", mode = "rb") as sec_file:
        return sec_file.read()

# %%  
def delete_accounts(filename, key, details):
    print("\t\t DELETING ACCOUNTS")
    while True:
        try:
            deleacc = int(input("Account number you want to delete: ")) - 1
            if deleacc < 0 or deleacc >= len(details):
                raise IndexError(f"NUMBER NOT IN RANGE...ONLY {len(details)}")
            break
        except ValueError:
            print("\tINVALID INPUT NOT AN INTEGER....TRY AGAIN")
        except IndexError as e:
            print(e)
    del details[deleacc]
    print("\n     PRINTING ALL ACC DETAILS")
    for i, accounts in enumerate(details, start = 1):
        print(f"\t{i}. {accounts['account']} ACCOUNT => USERNAME is {accounts['username']} => PASSWORD is {accounts['password']}")
    save_file("passwords.txt", details, key)


# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()