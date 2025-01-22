import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter
import os

class EncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryptor Tool")
        self.root.geometry("400x300")

        self.mode = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self.root, text="Select Encryption Mode and File")
        label.pack(pady=10)

        self.file_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.file_button.pack(pady=10)

        self.ecb_button = tk.Radiobutton(self.root, text="ECB Mode", variable=self.mode, value="ECB")
        self.cbc_button = tk.Radiobutton(self.root, text="CBC Mode", variable=self.mode, value="CBC")
        self.ctr_button = tk.Radiobutton(self.root, text="CTR Mode", variable=self.mode, value="CTR")
        
        self.ecb_button.pack()
        self.cbc_button.pack()
        self.ctr_button.pack()

        self.encrypt_button = tk.Button(self.root, text="Encrypt", command=self.encrypt_file)
        self.encrypt_button.pack(pady=20)

        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()

        self.filepath = ""

    def select_file(self):
        self.filepath = filedialog.askopenfilename(title="Select a File")
        if self.filepath:
            self.status_label.config(text=f"Selected File: {self.filepath}")

    def encrypt_file(self):
        if not self.filepath:
            messagebox.showerror("Error", "No file selected")
            return
        
        if not self.mode.get():
            messagebox.showerror("Error", "Please select an encryption mode")
            return

        key = get_random_bytes(16)  

        output_file = filedialog.asksaveasfilename(defaultextension=".enc", title="Save Encrypted File")
        if not output_file:
            return

        try:
            if self.mode.get() == "ECB":
                self.encrypt_ecb(self.filepath, output_file, key)
            elif self.mode.get() == "CBC":
                self.encrypt_cbc(self.filepath, output_file, key)
            elif self.mode.get() == "CTR":
                self.encrypt_ctr(self.filepath, output_file, key)
            
            messagebox.showinfo("Success", f"File encrypted successfully!\nSaved as: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def encrypt_ecb(self, input_file, output_file, key):
        cipher = AES.new(key, AES.MODE_ECB)
        with open(input_file, 'rb') as f:
            data = f.read()
            encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)

    def encrypt_cbc(self, input_file, output_file, key):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(input_file, 'rb') as f:
            data = f.read()
            encrypted_data = iv + cipher.encrypt(pad(data, AES.block_size))
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)

    def encrypt_ctr(self, input_file, output_file, key):
        ctr = Counter.new(128)
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        with open(input_file, 'rb') as f:
            data = f.read()
            encrypted_data = cipher.encrypt(data)
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptorApp(root)
    root.mainloop()
