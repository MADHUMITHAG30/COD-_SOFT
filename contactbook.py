
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Colorful Contact Book")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')
        
        # Data file
        self.data_file = "contacts.json"
        self.contacts = []
        self.load_contacts()
        
        # Colors
        self.colors = {
            'header': '#4682b4',
            'button': '#5f9ea0',
            'list_bg': '#e6e6fa',
            'entry_bg': '#ffffff',
            'highlight': '#b0e0e6'
        }
        
        # Create UI
        self.create_widgets()
    
    def load_contacts(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    self.contacts = json.load(f)
                except json.JSONDecodeError:
                    self.contacts = []
    
    def save_contacts(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.contacts, f, indent=2)
    
    def create_widgets(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.colors['header'], height=80)
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame, text="Contact Book",
            font=('Arial', 24, 'bold'),
            bg=self.colors['header'], fg='white'
        ).pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Contact list
        list_frame = tk.Frame(main_frame, bg=self.colors['list_bg'], bd=2, relief='groove')
        list_frame.pack(side='left', fill='y', padx=(0, 10))
        
        tk.Label(
            list_frame, text="Contacts",
            font=('Arial', 14, 'bold'),
            bg=self.colors['list_bg']
        ).pack(pady=10)
        
        self.contact_list = ttk.Treeview(list_frame, columns=('name', 'phone'), show='headings', height=20)
        self.contact_list.heading('name', text='Name')
        self.contact_list.heading('phone', text='Phone')
        self.contact_list.column('name', width=150)
        self.contact_list.column('phone', width=120)
        self.contact_list.pack(padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.contact_list.yview)
        self.contact_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        self.contact_list.bind('<<TreeviewSelect>>', self.display_contact_details)
        
        # Right panel - Contact details
        detail_frame = tk.Frame(main_frame, bg='#f0f8ff')
        detail_frame.pack(side='right', fill='both', expand=True)
        
        # Search frame
        search_frame = tk.Frame(detail_frame, bg='#f0f8ff')
        search_frame.pack(fill='x', pady=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, font=('Arial', 12),
            bg=self.colors['entry_bg'], bd=2, relief='groove'
        )
        search_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        search_btn = tk.Button(
            search_frame, text="Search",
            bg=self.colors['button'], fg='white',
            font=('Arial', 10, 'bold'),
            command=self.search_contact
        )
        search_btn.pack(side='left')
        
        # Contact details form
        form_frame = tk.LabelFrame(
            detail_frame, text="Contact Details",
            font=('Arial', 12, 'bold'),
            bg='#f0f8ff', bd=2, relief='groove'
        )
        form_frame.pack(fill='both', expand=True)
        
        labels = ['Name:', 'Phone:', 'Email:', 'Address:']
        self.entry_vars = {}
        
        for i, label in enumerate(labels):
            tk.Label(
                form_frame, text=label, bg='#f0f8ff', font=('Arial', 11)
            ).grid(row=i, column=0, sticky='e', pady=5, padx=5)
            var = tk.StringVar()
            entry = tk.Entry(
                form_frame, textvariable=var, font=('Arial', 11),
                bg=self.colors['entry_bg'], bd=1, relief='solid'
            )
            entry.grid(row=i, column=1, sticky='ew', pady=5, padx=5)
            self.entry_vars[label[:-1].lower()] = var
        
        # Button frame
        button_frame = tk.Frame(detail_frame, bg='#f0f8ff')
        button_frame.pack(fill='x', pady=(10, 0))
        
        buttons = [
            ('Add', self.add_contact, '#2e8b57'),
            ('Update', self.update_contact, '#4682b4'),
            ('Delete', self.delete_contact, '#cd5c5c'),
            ('Clear', self.clear_form, '#d2691e')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame, text=text, bg=color, fg='white',
                font=('Arial', 10, 'bold'), command=command
            )
            btn.pack(side='left', padx=5, ipadx=10, ipady=5)
        
        # Initialize contact list
        self.update_contact_list()
    
    def update_contact_list(self):
        self.contact_list.delete(*self.contact_list.get_children())
        for contact in self.contacts:
            self.contact_list.insert('', 'end', values=(contact['name'], contact['phone']))
    
    def display_contact_details(self, event):
        selected = self.contact_list.selection()
        if selected:
            contact = self.contacts[self.contact_list.index(selected[0])]
            for field, var in self.entry_vars.items():
                var.set(contact.get(field, ''))
    
    def add_contact(self):
        contact = {field: var.get().strip() for field, var in self.entry_vars.items()}
        if not contact['name']:
            messagebox.showerror("Error", "Name is required!")
            return
        
        self.contacts.append(contact)
        self.save_contacts()
        self.update_contact_list()
        self.clear_form()
        messagebox.showinfo("Success", "Contact added successfully!")
    
    def update_contact(self):
        selected = self.contact_list.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a contact to update!")
            return
        
        index = self.contact_list.index(selected[0])
        contact = {field: var.get().strip() for field, var in self.entry_vars.items()}
        if not contact['name']:
            messagebox.showerror("Error", "Name is required!")
            return
        
        self.contacts[index] = contact
        self.save_contacts()
        self.update_contact_list()
        messagebox.showinfo("Success", "Contact updated successfully!")
    
    def delete_contact(self):
        selected = self.contact_list.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a contact to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            index = self.contact_list.index(selected[0])
            del self.contacts[index]
            self.save_contacts()
            self.update_contact_list()
            self.clear_form()
            messagebox.showinfo("Success", "Contact deleted successfully!")
    
    def search_contact(self):
        query = self.search_var.get().lower()
        if not query:
            self.update_contact_list()
            return
        
        results = [
            contact for contact in self.contacts
            if query in contact['name'].lower() or query in contact['phone'].lower()
        ]
        
        self.contact_list.delete(*self.contact_list.get_children())
        for contact in results:
            self.contact_list.insert('', 'end', values=(contact['name'], contact['phone']))
    
    def clear_form(self):
        for var in self.entry_vars.values():
            var.set('')

def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
