
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Colorful Password Generator")
        self.root.geometry("500x480")
        self.root.configure(bg='#2c3e50')

        # Use consistent vars
        self.length_var = tk.IntVar(value=12)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.password_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg='#3498db', height=72)
        header.pack(fill='x')
        tk.Label(header, text="Password Generator", font=('Arial', 18, 'bold'),
                 bg='#3498db', fg='white').pack(pady=16)

        main = tk.Frame(self.root, bg='#2c3e50')
        main.pack(fill='both', expand=True, padx=20, pady=12)

        # Length label + scale
        tk.Label(main, text="Password Length:", font=('Arial', 12),
                 bg='#2c3e50', fg='#ecf0f1').pack(anchor='w', pady=(4,0))
        # Use tk.Scale for consistent behavior
        length_scale = tk.Scale(main, from_=8, to=32, orient='horizontal',
                                variable=self.length_var, bg='#2c3e50', fg='#ecf0f1',
                                troughcolor='#34495e', highlightthickness=0, length=320)
        length_scale.pack(pady=(0,6))
        # current length display
        self.length_display = tk.Label(main, text=str(self.length_var.get()),
                                       font=('Arial', 12, 'bold'), bg='#2c3e50', fg='#3498db')
        self.length_display.pack()
        # keep display in sync
        self.length_var.trace_add('write', lambda *_: self.length_display.config(text=str(self.length_var.get())))

        # Character options (checkboxes)
        opts = tk.Frame(main, bg='#2c3e50')
        opts.pack(pady=10, anchor='w')
        tk.Checkbutton(opts, text="Uppercase (A-Z)", variable=self.upper_var,
                       font=('Arial',10), bg='#2c3e50', fg='#ecf0f1',
                       selectcolor='#2c3e50', activebackground='#2c3e50').grid(row=0, column=0, sticky='w')
        tk.Checkbutton(opts, text="Lowercase (a-z)", variable=self.lower_var,
                       font=('Arial',10), bg='#2c3e50', fg='#ecf0f1',
                       selectcolor='#2c3e50', activebackground='#2c3e50').grid(row=1, column=0, sticky='w')
        tk.Checkbutton(opts, text="Digits (0-9)", variable=self.digits_var,
                       font=('Arial',10), bg='#2c3e50', fg='#ecf0f1',
                       selectcolor='#2c3e50', activebackground='#2c3e50').grid(row=2, column=0, sticky='w')
        tk.Checkbutton(opts, text="Symbols (!@#)", variable=self.symbols_var,
                       font=('Arial',10), bg='#2c3e50', fg='#ecf0f1',
                       selectcolor='#2c3e50', activebackground='#2c3e50').grid(row=3, column=0, sticky='w')

        # Generate button
        gen_btn = tk.Button(main, text="Generate Password", font=('Arial', 12, 'bold'),
                            bg='#3498db', fg='white', bd=0, padx=10, pady=8,
                            command=self.generate_password)
        gen_btn.pack(pady=14)

        # Password display entry (read-only look)
        password_entry = tk.Entry(main, textvariable=self.password_var, font=('Arial', 14),
                                  bd=0, relief='flat', bg='#34495e', fg='#2ecc71', justify='center')
        password_entry.pack(fill='x', ipady=10, padx=10)

        # Copy button
        copy_btn = tk.Button(main, text="Copy to Clipboard", font=('Arial', 11),
                             bg='#2ecc71', fg='black', bd=0, padx=8, pady=6,
                             command=self.copy_to_clipboard)
        copy_btn.pack(pady=10)

    def generate_password(self):
        try:
            length = int(self.length_var.get())
            chars = ''
            if self.upper_var.get():
                chars += string.ascii_uppercase
            if self.lower_var.get():
                chars += string.ascii_lowercase
            if self.digits_var.get():
                chars += string.digits
            if self.symbols_var.get():
                # Limit punctuation to common typable symbols to avoid weird clipboard issues
                safe_symbols = "!@#$%^&*()-_=+[]{};:,.<>?/~"
                chars += safe_symbols

            if not chars:
                messagebox.showerror("Error", "Please select at least one character type!")
                return

            # Guarantee at least one char of each selected type (optional — more secure)
            password_chars = []
            if self.upper_var.get():
                password_chars.append(random.choice(string.ascii_uppercase))
            if self.lower_var.get():
                password_chars.append(random.choice(string.ascii_lowercase))
            if self.digits_var.get():
                password_chars.append(random.choice(string.digits))
            if self.symbols_var.get():
                password_chars.append(random.choice(safe_symbols))

            # Fill the rest
            remaining = length - len(password_chars)
            if remaining > 0:
                password_chars += [random.choice(chars) for _ in range(remaining)]

            random.shuffle(password_chars)
            password = ''.join(password_chars[:length])
            self.password_var.set(password)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password:\n{e}")

    def copy_to_clipboard(self):
        pwd = self.password_var.get()
        if pwd:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(pwd)
                messagebox.showinfo("Success", "Password copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy:\n{e}")
        else:
            messagebox.showerror("Error", "No password to copy!")

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
