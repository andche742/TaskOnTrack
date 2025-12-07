import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry 
from controllers.task_controller import task_controller

class TaskPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.tasks = []
        self.next_id = 1  

        # layout columns
        self.columnconfigure(0, weight=0)   
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # main
        main = ttk.Frame(self, padding=20)
        main.grid(row=0, column=0, columnspan=2, sticky="nsew")
        main.columnconfigure(0, weight=1)

        # title
        title_row = ttk.Frame(main)
        title_row.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(
            title_row,
            text="Task List",
            font=("Helvetica", 18, "bold"),
        ).pack(side="left")

        # home button
        ttk.Button(
            title_row,
            text="Back to Dashboard",
            command=lambda: app.show_frame("DashboardPage"),
        ).pack(side="right")

        # task table
        table_frame = ttk.Frame(main)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("id", "name", "date", "description", "status")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Task Name")
        self.tree.heading("date", text="Date")
        self.tree.heading("description", text="Description")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=210)
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("description", width=80, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # add task form
        form_frame = ttk.LabelFrame(main, padding=10)
        form_frame.grid(row=3, column=0, sticky="ew", pady=(5, 0))
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Task Name").grid(row=0, column=0, sticky="w", pady=3)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Label(form_frame, text="Date").grid(row=1, column=0, sticky="w", pady=3)
        self.date_entry = DateEntry(
            form_frame,
            date_pattern="mm-dd-yyyy",  
        )
        self.date_entry.grid(row=1, column=1, sticky="w", pady=3)

        ttk.Label(form_frame, text="Description").grid(row=2, column=0, sticky="w", pady=3)
        self.description_entry = ttk.Entry(form_frame)
        self.description_entry.grid(row=2, column=1, sticky="ew", pady=3)

        self.output_text = tk.StringVar()
        self.output = ttk.Label(
            form_frame,
            textvariable=self.output_text,
            foreground='red',
            font=("Segoe UI", 12, "italic"),
        )

        # add, edit, delete buttons
        buttons_row = ttk.Frame(main)
        buttons_row.grid(row=4, column=0, sticky="e", pady=(8, 0))

        ttk.Button(
            buttons_row,
            text="Add Task",
            command=self.on_save,
            width=10,
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            buttons_row,
            text="Edit selected",

            command=self.on_edit_selected,
            width=12,
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            buttons_row,
            text="Delete selected",
            command=self.on_delete_selected,
            width=14,
        ).grid(row=0, column=2, padx=5)


    def on_save(self):
        name = self.name_entry.get().strip()
        date = self.date_entry.get().strip()
        description = self.description_entry.get().strip()

        if not name:
            self.output_text.set("Task name is required.")
            self.output.grid(row=6, column=0, pady=(0, 10))

            return
        if not date:
            self.output_text.set("Date is required.")
            self.output.grid(row=6, column=0, pady=(0, 10))
            return

        if not hasattr(self.app, 'current_user') or self.app.current_user is None:
            self.output_text.set("Please log in first.")
            self.output.grid(row=6, column=0, pady=(0, 10))
            return
            
        success, result = task_controller.create_task(self.app.current_user.id, name, date, description)

        if not success:
            self.output_text.set(result)
            self.output.grid(row=6, column=0, pady=(0, 10))

            return
        if success:
            self.refresh()

        # clear form (keep the date)
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.date_entry.set_date(date)

    def on_edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            self.output_text.set("No task selected.")
            self.output.grid(row=6, column=0, pady=(0, 10))
            return

        task_id = int(selected[0])
        success, task = task_controller.get_task_by_id(task_id)
        
        if not success:
            self.output_text.set(f"Error: {task}")
            self.output.grid(row=6, column=0, pady=(0, 10))

            return
        
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, task.title)
        
        self.date_entry.set_date(task.due_date)
        
        self.description_entry.delete(0, tk.END)
        if task.description:
            self.description_entry.insert(0, task.description)

        self.on_delete_selected()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not hasattr(self.app, 'current_user') or self.app.current_user is None:
            return
        
        user_id = self.app.current_user.id
        success, tasks = task_controller.get_tasks_by_user(user_id)
        
        if not success or not tasks:
            return
        
        for task in tasks:
            self.tree.insert(
                "",
                "end",
                iid=str(task.id),
                values=(
                    task.id,
                    task.title,
                    task.due_date,
                    task.description if task.description else "",
                    task.status
                )
            )

    def on_delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            self.output_text.set("No task selected.")
            self.output.grid(row=6, column=0, pady=(0, 10))
            return

        task_id = int(selected[0])
        success, result = task_controller.delete_task(task_id)
        
        if success:
            self.refresh()
        else:
            self.output_text.set(f"Error: {result}")
            self.output.grid(row=6, column=0, pady=(0, 10))
