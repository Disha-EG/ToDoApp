import tkinter as tk
from tkinter import messagebox, ttk
import json

class Task:
    def __init__(self, title, description, category):
        self.title = title
        self.description = description
        self.category = category
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __repr__(self):
        return f"Task({self.title}, {self.description}, {self.category}, {self.completed})"

# Load tasks from the JSON file
def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return [Task(**data) for data in json.load(f)]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to decode JSON. Please check the tasks.json file.")
        return []

# Save tasks to the JSON file
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do List")
        self.root.geometry("600x500")  # Set initial size of window
        self.root.configure(bg="#f4f4f9")
        self.root.resizable(True, True)  # Allow resizing the window

        self.tasks = load_tasks()

        # Set up the GUI components
        self.setup_ui()

    def setup_ui(self):
        # Title Label
        title_label = tk.Label(self.root, text="To-Do List", font=("Helvetica", 18, "bold"), bg="#f4f4f9")
        title_label.pack(pady=20, fill=tk.X)

        # Frame for task list
        list_frame = tk.Frame(self.root, bg="#f4f4f9")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Task Listbox
        self.task_listbox = tk.Listbox(list_frame, width=50, height=10, font=("Arial", 12), yscrollcommand=self.scrollbar.set, selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.task_listbox.yview)
        self.update_task_listbox()

        # Frame for task input
        input_frame = tk.Frame(self.root, bg="#f4f4f9")
        input_frame.pack(pady=10, fill=tk.X)

        # Task entry with placeholder
        self.task_entry = self.create_placeholder_entry(input_frame, "Enter task title", row=0)
        self.description_entry = self.create_placeholder_entry(input_frame, "Enter task description", row=1)

        # Category dropdown
        self.category_var = tk.StringVar()
        self.category_var.set("Personal")  # Default category
        self.category_menu = ttk.Combobox(input_frame, textvariable=self.category_var, values=["Personal", "Work", "Urgent"], font=("Arial", 12))
        self.category_menu.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Buttons
        button_frame = tk.Frame(self.root, bg="#f4f4f9")
        button_frame.pack(pady=20, fill=tk.X)

        add_button = tk.Button(button_frame, text="Add Task", command=self.add_task, bg="#28a745", fg="white", font=("Arial", 12, "bold"))
        add_button.grid(row=0, column=0, padx=20, pady=5, sticky="ew")

        complete_button = tk.Button(button_frame, text="Mark Completed", command=self.mark_completed, bg="#007bff", fg="white", font=("Arial", 12, "bold"))
        complete_button.grid(row=0, column=1, padx=20, pady=5, sticky="ew")

        delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task, bg="#dc3545", fg="white", font=("Arial", 12, "bold"))
        delete_button.grid(row=0, column=2, padx=20, pady=5, sticky="ew")

        clear_completed_button = tk.Button(button_frame, text="Clear Completed", command=self.clear_completed_tasks, bg="#ffc107", fg="black", font=("Arial", 12, "bold"))
        clear_completed_button.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        exit_button = tk.Button(button_frame, text="Exit", command=self.exit_app, bg="#6c757d", fg="white", font=("Arial", 12, "bold"))
        exit_button.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

    def create_placeholder_entry(self, parent, placeholder_text, row):
        """ Create an entry with placeholder text functionality. """
        entry = tk.Entry(parent, width=40, font=("Arial", 12))
        entry.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        entry.insert(0, placeholder_text)
        entry.bind("<FocusIn>", lambda event: self.on_focus_in(event, placeholder_text))
        entry.bind("<FocusOut>", lambda event: self.on_focus_out(event, placeholder_text))
        return entry

    def on_focus_in(self, event, placeholder_text):
        """ Remove placeholder text when the user focuses on the entry. """
        entry = event.widget
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg="black")  # Set text color to black when typing

    def on_focus_out(self, event, placeholder_text):
        """ Restore placeholder text if the entry is empty when focus is lost. """
        entry = event.widget
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg="gray")  # Set text color to gray for placeholder

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔" if task.completed else "✘"
            display_text = f"{task.title} ({task.category}) - {status}"
            self.task_listbox.insert(tk.END, display_text)

    def add_task(self):
        title = self.task_entry.get()
        description = self.description_entry.get()
        category = self.category_var.get()

        if title and title != "Enter task title" and description and description != "Enter task description":
            new_task = Task(title, description, category)
            self.tasks.append(new_task)
            save_tasks(self.tasks)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both title and description.")

    def mark_completed(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks[task_index].mark_completed()
            save_tasks(self.tasks)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            del self.tasks[task_index]
            save_tasks(self.tasks)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def clear_completed_tasks(self):
        self.tasks = [task for task in self.tasks if not task.completed]
        save_tasks(self.tasks)
        self.update_task_listbox()

    def exit_app(self):
        save_tasks(self.tasks)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
