""" Final Project  - Text Based Finance Tracker
    Designed by    - Hirumitha Kuladewa
    Student number - DSE-093
    Center name    - Orugodawatta Center """

# Importing Libraries and Modules 
import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkcalendar import DateEntry
from ttkthemes import ThemedStyle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# creating finance tracker app class
class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐨 Text-Based Finance Tracker 🐨") # App name

        # backend data saving
        self.file_path = 'E:/Software Engineering/7. Programming with python/Final Project/Final Project/Final Project 🕊/🙂Finance_Data🙂.json' # backend data saving path
        self.entries = self.load_data()
        self.selected_entries = set()

        # Background
        self.root.configure(bg="#AFC8AD") # background color

        # create the full interface 
        self.create_widgets()

    # Function for create gui using tkinter
    def create_widgets(self):
        style = ttk.Style() # style
        style.configure("My.TFrame", background="#88AB8E") # frame background color

        # Entry Frame
        entry_frame = ttk.Frame(self.root, padding="20", style="My.TFrame")
        entry_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Set Frame Label
        ttk.Label(entry_frame, text=f"Add/ Delete Entries", foreground="#F2FFE9", background="#88AB8E", font=('Helvetica', 16, 'bold', 'underline')).grid(row=0, column=0, columnspan=2, pady=10)

        # Entry Type
        ttk.Label(entry_frame, text="Entry Type               : ", foreground="black", background="#88AB8E", font=('Helvetica', 10, 'bold')).grid(row=2, column=0, padx=10, pady=5, sticky="w") # Creating a label for entry type
        
        # Create drop down to select income or expense
        entry_types = ["Income", "Expense"]
        self.entry_type_var = tk.StringVar(value=entry_types[0])
        entry_type_dropdown = ttk.Combobox(entry_frame, textvariable=self.entry_type_var, values=entry_types, state="readonly", style="My.TCombobox")
        entry_type_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Amount
        ttk.Label(entry_frame, text="Amount                   : ", foreground="black", background="#88AB8E", font=('Helvetica', 10, 'bold')).grid(row=3, column=0, padx=10, pady=5, sticky="w") # Creating a label for amount
        
        # Create entry box to add amount
        self.amount_var = tk.DoubleVar()
        self.amount_var.set("5000.0")
        self.amount_spinbox = ttk.Spinbox(entry_frame, from_=0, to=float('inf'), textvariable=self.amount_var, increment=1, width=15)
        self.amount_spinbox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Category
        ttk.Label(entry_frame, text="Category                 : ", foreground="black", background="#88AB8E", font=('Helvetica', 10, 'bold')).grid(row=4, column=0, padx=10, pady=5, sticky="w") # Creating a label for category
        
        # Set a cateegory you neeed
        self.category_var = tk.StringVar()
        category_combobox = ttk.Combobox(entry_frame, textvariable=self.category_var, values=self.get_all_categories())
        category_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        category_combobox.set("Sallery")

        # Date Entry
        ttk.Label(entry_frame, text="Date                        : ", foreground="black", background="#88AB8E", font=('Helvetica', 10, 'bold')).grid(row=5, column=0, padx=10, pady=5, sticky="w")  # Creating a label for set date
        self.date_entry = DateEntry(entry_frame, style="My.TEntry", date_pattern="yyyy-mm-dd") # Create calendar to add date
        self.date_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Add new record button
        ttk.Button(entry_frame, text="Add New Record to Entry", command=self.record_entry, style="Green.TButton").grid(row=6, columnspan=2, pady=10) # Button to add new record

        # Save entry button
        ttk.Button(entry_frame, text="Save Entries", command=self.save_entries_summary, style="Green.TButton").grid(row=7, columnspan=2, pady=10) # Button to save record where you want

        # Delete Button
        ttk.Button(entry_frame, text="Delete Selected Entries", command=self.delete_selected_entries, style="Red.TButton").grid(row=8, columnspan=2, pady=10) # Button to delete entries

        # Budget Frame
        budget_frame = ttk.Frame(self.root, padding="20", style="My.TFrame")
        budget_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # Create budget heading
        ttk.Label(budget_frame, text=f"Budget Settings", foreground="#F2FFE9", background="#88AB8E", font=('Helvetica', 16, 'bold', 'underline')).grid(row=0, column=0, columnspan=2, pady=10)

        # Set monthly budget
        ttk.Label(budget_frame, text="Set Monthly Budget   :", foreground="black", background="#88AB8E", font=('Helvetica', 10, 'bold')).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        # Create entry box to add budget
        self.budget_entry = ttk.Entry(budget_frame, style="My.TEntry")
        self.budget_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Button to set budget
        ttk.Button(budget_frame, text="Set Budget", command=self.set_budget, style="Purple.TButton").grid(row=3, columnspan=2, pady=10)

        # Remove Budget Button
        ttk.Button(budget_frame, text="Remove Monthly Budget", command=self.remove_budget, style="Red.TButton").grid(row=4, columnspan=2, pady=10)

        # Create Display Frame
        display_frame = ttk.Frame(self.root, padding="20", style="My.TFrame")
        display_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Display Frame Label
        ttk.Label(display_frame, text=f"Display Results", foreground="#F2FFE9", background="#88AB8E", font=('Helvetica', 16, 'bold', 'underline')).grid(row=0, column=0, columnspan=2, pady=10)

        # View all entries in Tree view
        columns = ("Select", "Type", "Amount", "Category", "Date") # Tree coloumns
        self.treeview = ttk.Treeview(display_frame, columns=columns, show="headings", selectmode="extended", style="My.Treeview")
        for col in columns:
            self.treeview.heading(col, text=col)
        self.treeview.grid(row=2, column=0, pady=10)

        # Scrollbar for Gridview
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.grid(row=2, column=1, sticky="ns")
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Button to view summary
        ttk.Button(display_frame, text="View Summary In Specific  Month", command=self.view_summary, style="Green.TButton").grid(row=3, column=0, pady=5)

        # Creating a analytics frame
        analytics_frame = ttk.Frame(self.root, padding="20", style="My.TFrame")
        analytics_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        # Create analytics heading
        ttk.Label(analytics_frame, text=f"View Analytics", foreground="#F2FFE9", background="#88AB8E", font=('Helvetica', 16, 'bold', 'underline')).grid(row=0, column=0, columnspan=2, pady=10)

        # Create a Figure and Axes for the bar graph
        self.fig, self.ax = plt.subplots(figsize=(6, 4), tight_layout=True)

        # Embed the matplotlib figure into the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=analytics_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, padx=10, pady=10)

        # Button to update the bar graph
        ttk.Button(analytics_frame, text="Update Analytics", command=self.update_analytics, style="Green.TButton").grid(row=2, column=0, pady=10)

        # Quit Button
        ttk.Button(self.root, text=f"Save data and Quit", command=self.quit_app, style="Red.TButton").grid(row=3, column=2, pady=10)

        # Running Text in the Footer
        self.running_text_var = tk.StringVar()
        running_text_label = ttk.Label(self.root, textvariable=self.running_text_var, font=('Helvetica', 10, 'bold'), foreground="gray", background="#AFC8AD")
        running_text_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Columns and rows in GUI
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(4, weight=0)

        # Populate Grid view
        self.update_treeview()

        # Start blinking running text
        self.blink_running_text()

    # Function for load data in json file
    def load_data(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            return data # get data from backend .json file
        else:
            return {'entries': [], 'budget': 0}

    # Set default categories 
    def get_all_categories(self):
        default_categories = ["Sallery", "Housing", "Transportation", "Utilities", "Food/ Supplies", "Pets", "Savings", "Entertainment", "Healthcare", "Insaurance", "Debt", "Gifts"]
        existing_categories = set(entry['category'] for entry in self.entries['entries'])
        all_categories = default_categories + list(existing_categories)
        return all_categories

    # Function to save data in backend
    def save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.entries, file, indent=2)

    # Function to record new entry
    def record_entry(self):
        entry_type = self.entry_type_var.get().lower()
        amount_str = float(self.amount_var.get())
        category = self.category_var.get()
        date_str = self.date_entry.get()

        # Error handling to amount
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error ❗", "Invalid amount. Please enter a valid numeric value.") # Show value error in message box
            return

        # Error handling to date
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error ❗", "Invalid date format. Please use YYYY-MM-DD.") # Show date error in message box
            return

        entry = {
            'type': entry_type,
            'amount': amount,
            'category': category,
            'date': date.strftime('%Y-%m-%d')
        }

        self.entries['entries'].append(entry)
        self.update_treeview()
        self.clear_entry_fields()
        self.show_running_text("Entry recorded successfully ✅")  # helping message in footer

    # Function for delete selected entries from grid and backend file
    def delete_selected_entries(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showwarning("No Selections ❗", "Please select entries to delete.") # Show not selected anything to delete error in message box
            return

        confirmed = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected entries?") # message box to ask confirm deleting selected entries
        if confirmed:
            entries_to_delete = [self.treeview.index(entry) for entry in selected_items]
            entries_to_delete.sort(reverse=True)

            for entry_index in entries_to_delete:
                if 0 <= entry_index < len(self.entries['entries']):
                    del self.entries['entries'][entry_index]

            self.save_data()
            self.update_treeview()
            self.show_running_text("Selected entries deleted successfully ✅") # helping message in footer

    # Function to clear entry fields
    def clear_entry_fields(self):
        self.entry_type_var.set("income")
        self.amount_var.set(5000.0)
        self.category_var.set("Sallery")
        self.date_entry.set_date(datetime.now())


    # Function for view summery in specific month
    def view_summary(self):
        month = simpledialog.askstring("Input", "Enter month (YYYY-MM):")  # Creating an input dialog for getting the specific month
        if month:
            monthly_entries = [entry for entry in self.entries['entries'] if entry['date'].startswith(month)]
            total_income, total_expenses, _, _ = self.calculate_totals({'entries': monthly_entries})
            summary = f"\nSummary for {month}\n\n"
            summary += f"Total Income  : {total_income}\n"
            summary += f"Total Expenses: {total_expenses}\n"
            summary += f"Net Income    : {total_income - total_expenses}\n"
            self.show_entries_window(f"Summary for {month}", summary)

    # Function for select file option to save data
    def save_entries_summary(self):
        file_options = [("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")] # File options
        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=file_options)
        if save_path:
            self.save_data_to_file(save_path)
            self.show_running_text(f"Entries and Summary saved successfully to {save_path} ✅") # helping message in footer

    # Function to save with selected file option
    def save_data_to_file(self, file_path):
        with open(file_path, 'w') as file:
            if file_path.endswith(".json"): # .json file save
                json.dump(self.entries, file, indent=2)
            elif file_path.endswith(".txt"): # .txt file save
                for entry in self.entries['entries']:
                    file.write(f"{entry}\n")

    # Function for set budget
    def set_budget(self):
        budget_amount_str = self.budget_entry.get()

        # Error handling to numeric value error
        try:
            budget_amount = float(budget_amount_str)
        except ValueError:
            messagebox.showerror("Error ❗", "Invalid budget amount. Please enter a valid numeric value.") # Message box for error
            return

        self.entries['budget'] = budget_amount
        self.save_data()
        self.show_running_text("Monthly budget set successfully ✅") # helping message in footer

    # Function to remove budget
    def remove_budget(self):
        confirmed = messagebox.askyesno("Confirm Removal", "Are you sure you want to remove the monthly budget?") # Message box for confirmation
        if confirmed:
            self.entries.pop('budget', None)
            self.save_data()
            self.show_running_text("Monthly budget removed successfully ❌") # helping message in footer

    # Function for calculating incomes, expenses, and budget
    def calculate_totals(self, entries):
        total_income = sum(entry['amount'] for entry in entries['entries'] if entry['type'] == 'income')
        total_expenses = sum(entry['amount'] for entry in entries['entries'] if entry['type'] == 'expense')
    
        # Check if 'budget' key exists in entries
        budget = entries.get('budget', 0)

        net_income = total_income - total_expenses - budget

        return total_income, total_expenses, budget, net_income
    
    # Function for update analytics
    def update_analytics(self):
        # Get total income, total expenses, and budget
        total_income, total_expenses, budget, net_income = self.calculate_totals(self.entries)

        # Data for the bar graph
        categories = ['Total Income', 'Total Expenses', 'Budget', 'Net Income']
        values = [total_income, total_expenses, budget, net_income]

        # Clear the previous plot
        self.ax.clear()

        # Plot the bar graph
        self.ax.bar(categories, values, color=['green', 'red', 'purple', 'blue'])

        # Set labels and title
        self.ax.set_ylabel('Amount')
        self.ax.set_title('Financial Analytics')

        # Embed the updated graph into the Tkinter window
        self.canvas.draw()

    # Function for exiting from app
    def quit_app(self):
        confirmed = messagebox.askyesno("Confirm Exit", "Do you want to save data and quit?")  # Confirmation message box

        if confirmed:
            self.save_data()
            self.root.destroy()

    # Function for get all entries
    def get_all_entries_text(self):
        entries_text = ""
        for entry in self.entries['entries']:
            entries_text += str(entry) + "\n"
        return entries_text

    # Function for entry window
    def show_entries_window(self, title, text):
        entries_window = tk.Toplevel(self.root)
        entries_window.title(title)
        entries_label = tk.Label(entries_window, text=text)
        entries_label.pack(padx=10, pady=10)

    # Function for update the grid view
    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        for i, entry in enumerate(self.entries['entries']):
            values = (f"{i + 1}", entry['type'], entry['amount'], entry['category'], entry['date'])
            self.treeview.insert("", "end", values=values)

    # Function for helping messages
    def show_running_text(self, text):
        self.running_text_var.set(text)
        self.root.after(3000, lambda: self.running_text_var.set(""))
        
    def blink_running_text(self):
        current_text = self.running_text_var.get()
        if current_text == "Money is not the life, but make sure how to use money.":
            self.running_text_var.set("Designed by Hirumitha Kuladewa")
        else:
            self.running_text_var.set("Money is not the life, but make sure how to use money.")
        
        self.root.after(1000, self.blink_running_text)

# main
if __name__ == "__main__":
    root = tk.Tk()

    # styles
    root.style = ThemedStyle(root)
    root.style.set_theme("plastik")
    root.style.configure("Green.TButton", foreground="green", font=('Helvetica', 10, 'bold'))
    root.style.configure("Red.TButton", foreground="red", font=('Helvetica', 10, 'bold'))
    root.style.configure("Purple.TButton", foreground="purple", font=('Helvetica', 10, 'bold'))
    root.style.configure("Blue.TButton", foreground="blue", font=('Helvetica', 10, 'bold'))
    root.style.configure("My.TEntry", fieldbackground="#C1F2B0")
    root.style.configure("My.Treeview", background="#C1F2B0")

    app = FinanceTrackerApp(root)
    root.mainloop()