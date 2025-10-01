
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from cryptography.fernet import Fernet
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Helper to center and resize window to half the screen
def set_half_screen(root):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

# Helper to center and resize window to half the screen
def set_half_main_window(win, parent):
    parent.update_idletasks()
    geom = parent.geometry()
    # geom is like 'WxH+X+Y'
    try:
        w_h, x_y = geom.split('+', 1)
        width, height = map(int, w_h.split('x'))
        x, y = map(int, x_y.split('+'))
        half_width = width // 2
        half_height = height // 2
        new_x = x + (width - half_width) // 2
        new_y = y + (height - half_height) // 2
        win.geometry(f"{half_width}x{half_height}+{new_x}+{new_y}")
    except Exception:
        # fallback: center on screen
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        width = screen_width // 4
        height = screen_height // 4
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")

# --- Encryption/Decryption and File Logic (from passwds.py) ---
def load_key():
    with open(os.path.join(BASE_DIR, "secret_key.txt"), mode="rb") as sec_file:
        return sec_file.read()

def encrypt(crypt_word, key):
    f = Fernet(key)
    encrypted = f.encrypt(crypt_word.encode())
    return encrypted.decode()

def de_crypt(enc_words, key):
    f = Fernet(key)
    decrypt = f.decrypt(enc_words.encode())
    return decrypt.decode()

def load_file(filename, key):
    try:
        details = []
        with open(filename, mode="r") as file:
            for accounts in file:
                jina, usern, passc = [value.strip() for value in accounts.strip().split(",")]
                dename = de_crypt(jina, key)
                deuser = de_crypt(usern, key)
                depass = de_crypt(passc, key)
                dis1 = {"account": dename, "username": deuser, "password": depass}
                details.append(dis1)
        return details
    except FileNotFoundError:
        return [
            {"account": "Email", "username": "ryankamau@gmail.com", "password": "LETsgo"},
            {"account": "Youtube", "username": "ryan", "password": "Whatdidimiss"}
        ]

def save_file(filename, details, key):
    Edetails = []
    for accounts in details:
        crypt1, crypt2, crypt3 = accounts['account'], accounts['username'], accounts['password']
        encrypt1, encrypt2, encrypt3 = encrypt(crypt1, key), encrypt(crypt2, key), encrypt(crypt3, key)
        enc_accounts = {"account": encrypt1, "username": encrypt2, "password": encrypt3}
        Edetails.append(enc_accounts)
    with open(filename, mode="w") as file:
        for accounts in Edetails:
            file.write(f"{accounts['account']}, {accounts['username']}, {accounts['password']}\n")

# --- GUI Application ---
class AccountManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Account Manager (Encrypted)")
        self.key = load_key()
        self.filename = os.path.join(BASE_DIR, "passwds.txt")
        self.details = load_file(self.filename, self.key)
        self.setup_main_menu()

    def setup_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()
        tk.Label(frame, text="Account Manager", font=("Arial", 18, "bold")).pack(pady=10)
        ttk.Button(frame, text="Display Details", width=30, command=self.display_details).pack(pady=5)
        ttk.Button(frame, text="Add Account Details", width=30, command=self.add_account).pack(pady=5)
        ttk.Button(frame, text="Update Account Details", width=30, command=self.update_details).pack(pady=5)
        ttk.Button(frame, text="Delete Account", width=30, command=self.delete_account).pack(pady=5)
        ttk.Button(frame, text="Save to File", width=30, command=self.save_to_file).pack(pady=5)
        ttk.Button(frame, text="Exit", width=30, command=self.root.quit).pack(pady=5)

    def display_details(self):
        win = tk.Toplevel(self.root)
        win.title("All Account Details")
        cols = ("#", "Account", "Username", "Password")
        tree = ttk.Treeview(win, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=80 if col == "#" else 150)
        for idx, acc in enumerate(self.details, start=1):
            tree.insert('', 'end', values=(idx, acc['account'], acc['username'], acc['password']))
        tree.pack(expand=True, fill='both', padx=10, pady=10)
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=5)
        set_half_main_window(win, self.root)

    def add_account(self):
        def add():
            acc = acc_var.get().strip().title()
            user = user_var.get().strip()
            psw = psw_var.get().strip()
            if not acc or not user or not psw:
                messagebox.showerror("Error", "All fields are required.")
                return
            self.details.append({"account": acc, "username": user, "password": psw})
            messagebox.showinfo("Success", "Account added.")
            win.destroy()
        win = tk.Toplevel(self.root)
        win.title("Add Account")
        acc_var, user_var, psw_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
        tk.Label(win, text="Account:").pack(pady=2)
        tk.Entry(win, textvariable=acc_var).pack(pady=2)
        tk.Label(win, text="Username:").pack(pady=2)
        tk.Entry(win, textvariable=user_var).pack(pady=2)
        tk.Label(win, text="Password:").pack(pady=2)
        tk.Entry(win, textvariable=psw_var, show='*').pack(pady=2)
        ttk.Button(win, text="Add", command=add).pack(pady=10)
        ttk.Button(win, text="Cancel", command=win.destroy).pack()
        set_half_main_window(win, self.root)

    def update_details(self):
        if not self.details:
            messagebox.showinfo("Info", "No accounts to update.")
            return
        win = tk.Toplevel(self.root)
        win.title("Update Account")
        tk.Label(win, text="Select account to update:").pack(pady=5)
        accounts = [f"{i+1}. {d['account']} ({d['username']})" for i, d in enumerate(self.details)]
        sel_var = tk.StringVar(value=accounts)
        listbox = tk.Listbox(win, listvariable=sel_var, height=8, width=40)
        listbox.pack(pady=5)
        def update():
            idx = listbox.curselection()
            if not idx:
                messagebox.showerror("Error", "Select an account.")
                return
            idx = idx[0]
            acc = self.details[idx]
            field = simpledialog.askinteger("Field", "Change:\n1 - Username\n2 - Password", parent=win, minvalue=1, maxvalue=2)
            if field == 1:
                new_user = simpledialog.askstring("Username", "Enter new username:", parent=win)
                if new_user:
                    acc['username'] = new_user
            elif field == 2:
                new_psw = simpledialog.askstring("Password", "Enter new password:", parent=win, show='*')
                if new_psw:
                    acc['password'] = new_psw
            messagebox.showinfo("Success", "Account updated.")
            win.destroy()
        ttk.Button(win, text="Update", command=update).pack(pady=5)
        ttk.Button(win, text="Cancel", command=win.destroy).pack()
        set_half_main_window(win, self.root)

    def delete_account(self):
        if not self.details:
            messagebox.showinfo("Info", "No accounts to delete.")
            return
        win = tk.Toplevel(self.root)
        win.title("Delete Account")
        tk.Label(win, text="Select account to delete:").pack(pady=5)
        accounts = [f"{i+1}. {d['account']} ({d['username']})" for i, d in enumerate(self.details)]
        sel_var = tk.StringVar(value=accounts)
        listbox = tk.Listbox(win, listvariable=sel_var, height=8, width=40)
        listbox.pack(pady=5)
        def delete():
            idx = listbox.curselection()
            if not idx:
                messagebox.showerror("Error", "Select an account.")
                return
            idx = idx[0]
            del self.details[idx]
            messagebox.showinfo("Success", "Account deleted.")
            win.destroy()
        ttk.Button(win, text="Delete", command=delete).pack(pady=5)
        ttk.Button(win, text="Cancel", command=win.destroy).pack()
        set_half_main_window(win, self.root)

    def save_to_file(self):
        save_file(self.filename, self.details, self.key)
        messagebox.showinfo("Saved", "All details saved to file (encrypted).")

if __name__ == "__main__":
    root = tk.Tk()
    set_half_screen(root)
    app = AccountManagerGUI(root)
    root.mainloop()
    