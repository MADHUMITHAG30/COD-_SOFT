
import json
import os
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox

class ToDoList:
    def __init__(self, filename="todo.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                try:
                    self.tasks = json.load(f)
                except json.JSONDecodeError:
                    # if file is empty or invalid, start with empty list
                    self.tasks = []

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4, default=str)

    def add_task(self, description, priority="medium", due_date=None):
        # compute next id robustly (handles deletions)
        next_id = max((task.get("id", 0) for task in self.tasks), default=0) + 1
        task = {
            "id": next_id,
            "description": description,
            "priority": priority.lower(),
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_tasks(self, show_completed=False):
        if not show_completed:
            return [task for task in self.tasks if not task.get("completed", False)]
        return self.tasks

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.get("id") == task_id:
                task["completed"] = True
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        original_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.get("id") != task_id]
        # re-number IDs if you want continuous ids (optional). I'll reassign so UI stays consistent.
        for i, task in enumerate(self.tasks, 1):
            task["id"] = i
        self.save_tasks()
        return len(self.tasks) != original_len

    def clear_completed(self):
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task.get("completed", False)]
        for i, task in enumerate(self.tasks, 1):
            task["id"] = i
        self.save_tasks()
        return initial_count - len(self.tasks)

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("900x600")
        self.todo = ToDoList()
        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        add_frame = LabelFrame(self.root, text="Add New Task", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)
        
        Label(add_frame, text="Description:").grid(row=0, column=0, sticky="e")
        self.description_entry = Entry(add_frame, width=60)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)
        
        Label(add_frame, text="Priority:").grid(row=1, column=0, sticky="e")
        self.priority_var = StringVar(value="medium")
        priorities = ["low", "medium", "high"]
        self.priority_menu = OptionMenu(add_frame, self.priority_var, *priorities)
        self.priority_menu.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        Label(add_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e")
        self.due_date_entry = Entry(add_frame, width=20)
        self.due_date_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        add_button = Button(add_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        list_frame = LabelFrame(self.root, text="Task List", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.task_tree = ttk.Treeview(
            list_frame,
            columns=("id", "description", "priority", "due_date", "status"),
            show="headings",
            selectmode="browse"
        )
        self.task_tree.heading("id", text="ID")
        self.task_tree.heading("description", text="Description")
        self.task_tree.heading("priority", text="Priority")
        self.task_tree.heading("due_date", text="Due Date")
        self.task_tree.heading("status", text="Status")
        self.task_tree.column("id", width=50, anchor="center")
        self.task_tree.column("description", width=400)
        self.task_tree.column("priority", width=100, anchor="center")
        self.task_tree.column("due_date", width=120, anchor="center")
        self.task_tree.column("status", width=100, anchor="center")
        self.task_tree.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        action_frame = Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        complete_button = Button(action_frame, text="Mark Complete", command=self.complete_task)
        complete_button.pack(side="left", padx=5)
        
        delete_button = Button(action_frame, text="Delete Task", command=self.delete_task)
        delete_button.pack(side="left", padx=5)
        
        clear_button = Button(action_frame, text="Clear Completed", command=self.clear_completed)
        clear_button.pack(side="left", padx=5)
        
        self.show_completed_var = IntVar()
        show_completed_check = Checkbutton(
            action_frame, text="Show Completed", variable=self.show_completed_var,
            command=self.refresh_task_list
        )
        show_completed_check.pack(side="right", padx=5)

        # Double-click to toggle complete (optional UX)
        self.task_tree.bind("<Double-1>", lambda e: self.complete_task())

    def refresh_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        show_completed = bool(self.show_completed_var.get())
        tasks = self.todo.get_tasks(show_completed)
        
        for task in tasks:
            status = "Completed" if task.get("completed") else "Pending"
            due = task.get("due_date") if task.get("due_date") else ""
            self.task_tree.insert("", "end", values=(
                task.get("id"),
                task.get("description"),
                task.get("priority", "").capitalize(),
                due,
                status
            ))

    def add_task(self):
        description = self.description_entry.get().strip()
        if not description:
            messagebox.showerror("Error", "Task description cannot be empty")
            return
        
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get().strip()
        
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                return
        
        self.todo.add_task(description, priority, due_date if due_date else None)
        self.description_entry.delete(0, END)
        self.due_date_entry.delete(0, END)
        self.refresh_task_list()
        messagebox.showinfo("Success", "Task added successfully")

    def _get_selected_task_id(self):
        selected = self.task_tree.selection()
        if not selected:
            return None
        item_id = selected[0]
        values = self.task_tree.item(item_id, "values")
        if not values:
            return None
        try:
            return int(values[0])
        except (ValueError, TypeError):
            return None

    def complete_task(self):
        task_id = self._get_selected_task_id()
        if task_id is None:
            messagebox.showerror("Error", "Please select a task to complete")
            return
        
        if self.todo.complete_task(task_id):
            self.refresh_task_list()
            messagebox.showinfo("Success", f"Task {task_id} marked as completed")
        else:
            messagebox.showerror("Error", f"Task {task_id} not found")

    def delete_task(self):
        task_id = self._get_selected_task_id()
        if task_id is None:
            messagebox.showerror("Error", "Please select a task to delete")
            return
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete task {task_id}?"):
            if self.todo.delete_task(task_id):
                self.refresh_task_list()
                messagebox.showinfo("Success", f"Task {task_id} deleted")
            else:
                messagebox.showerror("Error", f"Task {task_id} not found")

    def clear_completed(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all completed tasks?"):
            removed = self.todo.clear_completed()
            self.refresh_task_list()
            messagebox.showinfo("Success", f"Removed {removed} completed tasks")

def main():
    root = Tk()
    app = ToDoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
