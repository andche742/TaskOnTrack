import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry 


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


        # MAIN CONTENT AREA
        main = ttk.Frame(self, padding=20)
        main.grid(row=0, column=0, columnspan=2, sticky="nsew")
        main.columnconfigure(0, weight=1)

        # Title row
        title_row = ttk.Frame(main)
        title_row.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(
            title_row,
            text="Task List",
            font=("Helvetica", 18, "bold"),
        ).pack(side="left")

        ttk.Button(
            title_row,
            text="Back to Dashboard",
            command=lambda: app.show_frame("DashboardPage"),
        ).pack(side="right")

        # Task table 
        table_frame = ttk.Frame(main)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("name", "date", "time", "status")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
        )

        self.tree.heading("name", text="Task Name")
        self.tree.heading("date", text="Date")
        self.tree.heading("time", text="Time")
        self.tree.heading("status", text="Status")

        # column widths (can tweak later)
        self.tree.column("name", width=260)
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("time", width=80, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # "Add New Task" button 
        add_btn_row = ttk.Frame(main)
        add_btn_row.grid(row=2, column=0, sticky="ew", pady=(10, 5))

        ttk.Button(
            add_btn_row,
            text="Add New Task",
            command=self.focus_task_form,
        ).pack(anchor="center")

        # Add Task form 
        form_frame = ttk.LabelFrame(main, text="Add New Task", padding=10)
        form_frame.grid(row=3, column=0, sticky="ew", pady=(5, 0))
        form_frame.columnconfigure(1, weight=1)

        # Task Name
        ttk.Label(form_frame, text="Task Name").grid(row=0, column=0, sticky="w", pady=3)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", pady=3)

        # Date
        ttk.Label(form_frame, text="Date").grid(row=1, column=0, sticky="w", pady=3)
        self.date_entry = DateEntry(
            form_frame,
            date_pattern="yyyy-mm-dd",  
        )
        self.date_entry.grid(row=1, column=1, sticky="w", pady=3)

        # Time
        ttk.Label(form_frame, text="Time (HH:MM)").grid(row=2, column=0, sticky="w", pady=3)
        self.time_entry = ttk.Entry(form_frame)
        self.time_entry.grid(row=2, column=1, sticky="ew", pady=3)

        # Status dropdown
        ttk.Label(form_frame, text="Status").grid(row=3, column=0, sticky="w", pady=3)
        self.status_var = tk.StringVar(value="Todo")
        self.status_combo = ttk.Combobox(
            form_frame,
            textvariable=self.status_var,
            values=["Todo", "In Progress", "Done"],
            state="readonly",
        )
        self.status_combo.grid(row=3, column=1, sticky="w", pady=3)

        # Save / View / Delete buttons 
        buttons_row = ttk.Frame(main)
        buttons_row.grid(row=4, column=0, sticky="e", pady=(8, 0))

        ttk.Button(
            buttons_row,
            text="Save",
            command=self.on_save,
            width=10,
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            buttons_row,
            text="View selected",
            command=self.on_view_selected,
            width=12,
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            buttons_row,
            text="Delete selected",
            command=self.on_delete_selected,
            width=14,
        ).grid(row=0, column=2, padx=5)


    #  Handlers 

    def focus_task_form(self):
        """Move cursor to Task Name entry when 'Add New Task' is clicked."""
        self.name_entry.focus_set()

    def on_save(self):
        """Add a new task from the form into the table (for now, in memory)."""
        name = self.name_entry.get().strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        status = self.status_var.get()

        if not name:
            print("Task name is required.")
            return

        task = {
            "id": self.next_id,
            "name": name,
            "date": date,
            "time": time,
            "status": status,
        }
        self.next_id += 1
        self.tasks.append(task)

        # insert into Treeview
        self.tree.insert(
            "",
            "end",
            iid=str(task["id"]),
            values=(task["name"], task["date"], task["time"], task["status"]),
        )

        # clear form (keep the date)
        self.name_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.date_entry.set_date(date)
        self.status_var.set("Todo")

    def on_view_selected(self):
        """Load selected task into the form fields."""
        selected = self.tree.selection()
        if not selected:
            return

        iid = selected[0]
        task = next((t for t in self.tasks if str(t["id"]) == iid), None)
        if task is None:
            return

        # fill form with the task data
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, task["name"])

        self.date_entry.set_date(task["date"])

        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, task["time"])

        self.status_var.set(task["status"])

    def on_delete_selected(self):
        """Delete selected task from table and in-memory list."""
        selected = self.tree.selection()
        if not selected:
            return

        iid = selected[0]
        self.tree.delete(iid)
        self.tasks = [t for t in self.tasks if str(t["id"]) != iid]
