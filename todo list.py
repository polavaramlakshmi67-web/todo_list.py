import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.tasks = []
        self.filename = "tasks.json"
        
        # Load existing tasks
        self.load_tasks()
        
        # Configure colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#4a90e2"
        self.success_color = "#5cb85c"
        self.danger_color = "#d9534f"
        
        self.root.configure(bg=self.bg_color)
        
        self.create_widgets()
        self.refresh_task_list()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="📝 My To-Do List", 
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Task entry
        self.task_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=40,
            relief=tk.FLAT,
            bd=2
        )
        self.task_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=8)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="Add Task",
            font=("Arial", 11, "bold"),
            bg=self.primary_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_task,
            padx=20,
            pady=8
        )
        add_btn.pack(side=tk.LEFT)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg=self.bg_color)
        stats_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Total: 0 | Completed: 0 | Pending: 0",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#666"
        )
        self.stats_label.pack()
        
        # Task list frame with scrollbar
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Task listbox
        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 11),
            height=15,
            selectmode=tk.SINGLE,
            relief=tk.FLAT,
            bd=2,
            yscrollcommand=scrollbar.set
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20, padx=20)
        
        # Complete button
        complete_btn = tk.Button(
            btn_frame,
            text="✓ Complete",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.complete_task,
            padx=15,
            pady=8
        )
        complete_btn.grid(row=0, column=0, padx=5)
        
        # Delete button
        delete_btn = tk.Button(
            btn_frame,
            text="🗑 Delete",
            font=("Arial", 10, "bold"),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.delete_task,
            padx=15,
            pady=8
        )
        delete_btn.grid(row=0, column=1, padx=5)
        
        # Clear completed button
        clear_btn = tk.Button(
            btn_frame,
            text="Clear Completed",
            font=("Arial", 10, "bold"),
            bg="#f0ad4e",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_completed,
            padx=15,
            pady=8
        )
        clear_btn.grid(row=0, column=2, padx=5)
        
        # Clear all button
        clear_all_btn = tk.Button(
            btn_frame,
            text="Clear All",
            font=("Arial", 10, "bold"),
            bg="#777",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_all,
            padx=15,
            pady=8
        )
        clear_all_btn.grid(row=0, column=3, padx=5)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
        task = {
            "text": task_text,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_task_list()
        
    def complete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.save_tasks()
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            task_text = self.tasks[index]["text"]
            
            if messagebox.askyesno("Confirm", f"Delete task: '{task_text}'?"):
                del self.tasks[index]
                self.save_tasks()
                self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def clear_completed(self):
        completed_count = sum(1 for task in self.tasks if task["completed"])
        
        if completed_count == 0:
            messagebox.showinfo("Info", "No completed tasks to clear!")
            return
        
        if messagebox.askyesno("Confirm", f"Clear {completed_count} completed task(s)?"):
            self.tasks = [task for task in self.tasks if not task["completed"]]
            self.save_tasks()
            self.refresh_task_list()
    
    def clear_all(self):
        if not self.tasks:
            messagebox.showinfo("Info", "No tasks to clear!")
            return
        
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            self.tasks = []
            self.save_tasks()
            self.refresh_task_list()
    
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        
        for task in self.tasks:
            status = "✓" if task["completed"] else "○"
            display_text = f"{status} {task['text']}"
            self.task_listbox.insert(tk.END, display_text)
            
            # Change color for completed tasks
            if task["completed"]:
                self.task_listbox.itemconfig(tk.END, fg="#999", selectbackground="#ddd")
        
        # Update statistics
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["completed"])
        pending = total - completed
        
        self.stats_label.config(
            text=f"Total: {total} | Completed: {completed} | Pending: {pending}"
        )
    
    def save_tasks(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
                self.tasks = []

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()