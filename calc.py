
import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("400x400")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Number entry fields
        tk.Label(self.root, text="First Number:").pack(pady=5)
        self.num1_entry = tk.Entry(self.root)
        self.num1_entry.pack(pady=5)
        
        tk.Label(self.root, text="Second Number:").pack(pady=5)
        self.num2_entry = tk.Entry(self.root)
        self.num2_entry.pack(pady=5)
        
        # Operation buttons frame
        operations_frame = tk.Frame(self.root)
        operations_frame.pack(pady=10)
        
        tk.Button(operations_frame, text="+", width=5, command=lambda: self.calculate('+')).grid(row=0, column=0, padx=5)
        tk.Button(operations_frame, text="-", width=5, command=lambda: self.calculate('-')).grid(row=0, column=1, padx=5)
        tk.Button(operations_frame, text="*", width=5, command=lambda: self.calculate('*')).grid(row=0, column=2, padx=5)
        tk.Button(operations_frame, text="/", width=5, command=lambda: self.calculate('/')).grid(row=0, column=3, padx=5)
        
        # Result display
        self.result_label = tk.Label(self.root, text="", font=('Arial', 14))
        self.result_label.pack(pady=20)
        
        # Clear button
        tk.Button(self.root, text="Clear", command=self.clear_fields).pack(pady=10)
    
    def calculate(self, operation):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            
            if operation == '+':
                result = num1 + num2
                self.result_label.config(text=f"Result: {num1} + {num2} = {result}")
            elif operation == '-':
                result = num1 - num2
                self.result_label.config(text=f"Result: {num1} - {num2} = {result}")
            elif operation == '*':
                result = num1 * num2
                self.result_label.config(text=f"Result: {num1} * {num2} = {result}")
            elif operation == '/':
                if num2 == 0:
                    messagebox.showerror("Error", "Division by zero is not allowed!")
                    return
                result = num1 / num2
                self.result_label.config(text=f"Result: {num1} / {num2} = {result}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def clear_fields(self):
        self.num1_entry.delete(0, tk.END)
        self.num2_entry.delete(0, tk.END)
        self.result_label.config(text="")

def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
