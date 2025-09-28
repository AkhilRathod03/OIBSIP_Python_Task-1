import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from bmi_logic import calculate_bmi, classify_bmi
from database import save_bmi_record, get_user_history
from charts import plot_bmi_trend

class BMIGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("800x850") # Increased height for history
        tb.Style(theme='superhero')

        # Define styles
        self.font_label = ("Helvetica", 12, "bold")
        self.font_entry = ("Helvetica", 12)
        self.font_header = ("Helvetica", 28, "bold")
        self.font_result = ("Helvetica", 20, "bold")
        self.font_category = ("Helvetica", 16, "bold")

        self.create_widgets()

    def create_widgets(self):
        main_frame = tb.Frame(self.root, padding=(20, 15))
        main_frame.pack(fill=BOTH, expand=YES)

        top_frame = tb.Frame(main_frame)
        top_frame.pack(fill=X)

        header = tb.Label(top_frame, text="BMI Calculator", font=self.font_header, bootstyle=PRIMARY)
        header.pack(pady=(10, 20))

        # --- Input Frame ---
        input_frame = tb.Labelframe(top_frame, text="Your Details", bootstyle=INFO, padding=15)
        input_frame.pack(pady=10, padx=10, fill=X)
        # ... (rest of the input widgets are the same)
        self.name_label = tb.Label(input_frame, text="Name:", font=self.font_label)
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = tb.Entry(input_frame, font=self.font_entry, bootstyle=SUCCESS)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.age_label = tb.Label(input_frame, text="Age:", font=self.font_label)
        self.age_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.age_entry = tb.Entry(input_frame, font=self.font_entry, bootstyle=SUCCESS)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.weight_label = tb.Label(input_frame, text="Weight (kg):", font=self.font_label)
        self.weight_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.weight_entry = tb.Entry(input_frame, font=self.font_entry, bootstyle=SUCCESS)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.height_label = tb.Label(input_frame, text="Height (m):", font=self.font_label)
        self.height_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.height_entry = tb.Entry(input_frame, font=self.font_entry, bootstyle=SUCCESS)
        self.height_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        input_frame.columnconfigure(1, weight=1)

        # --- Button Frame ---
        button_frame = tb.Frame(top_frame)
        button_frame.pack(pady=20)
        style = tb.Style()
        style.configure('TButton', font=self.font_label)
        self.calc_button = tb.Button(button_frame, text="Calculate", command=self.calculate_and_display, bootstyle=PRIMARY, width=12)
        self.calc_button.grid(row=0, column=0, padx=5)
        self.save_button = tb.Button(button_frame, text="Save", command=self.save_record, bootstyle=SUCCESS, width=12)
        self.save_button.grid(row=0, column=1, padx=5)
        self.trends_button = tb.Button(button_frame, text="Show Trends", command=self.show_trends, bootstyle=WARNING, width=12)
        self.trends_button.grid(row=0, column=2, padx=5)

        # --- Result Frame ---
        result_frame = tb.Labelframe(top_frame, text="Result", bootstyle=INFO, padding=15)
        result_frame.pack(pady=10, padx=10, fill=X)
        self.result_label = tb.Label(result_frame, text="", font=self.font_result, anchor="center")
        self.result_label.pack(pady=5, fill=X)
        self.category_label = tb.Label(result_frame, text="", font=self.font_category, anchor="center")
        self.category_label.pack(pady=5, fill=X)

        # --- History Frame ---
        history_frame = tb.Labelframe(main_frame, text="User History", bootstyle=INFO, padding=15)
        history_frame.pack(pady=10, padx=10, fill=BOTH, expand=YES)

        cols = ["Date", "BMI", "Category", "Weight (kg)", "Height (m)", "Age"]
        self.history_tree = tb.Treeview(history_frame, columns=cols, show='headings', bootstyle=PRIMARY)
        for col in cols:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100, anchor=CENTER)
        self.history_tree.pack(fill=BOTH, expand=YES)

    def calculate_and_display(self):
        # This function remains largely the same
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if not (0 < weight < 500 and 0 < height < 3):
                raise ValueError("Input values are out of realistic range.")
            self.bmi = calculate_bmi(weight, height)
            self.category = classify_bmi(self.bmi)
            self.result_label.config(text=f"BMI: {self.bmi}")
            self.category_label.config(text=f"Category: {self.category}", bootstyle=self.get_category_style(self.category))
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter valid numbers for weight and height. {e}")
            self.bmi = None
            self.category = None

    def get_category_style(self, category):
        # This function remains the same
        if category == "Underweight": return WARNING
        elif category == "Normal weight": return SUCCESS
        elif category == "Overweight": return WARNING
        elif category == "Obese": return DANGER
        return DEFAULT

    def save_record(self):
        # This function remains largely the same, but now refreshes history
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Missing Name", "Please enter a name to save the record.")
            return
        if not hasattr(self, 'bmi') or self.bmi is None:
            self.calculate_and_display()
            if self.bmi is None: return
        try:
            age = int(self.age_entry.get()) if self.age_entry.get() else 0
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if save_bmi_record(name, age, weight, height, self.bmi, self.category):
                messagebox.showinfo("Success", "Your BMI record has been saved.")
                self.view_history() # Refresh history view after saving
            else:
                messagebox.showerror("Database Error", "Failed to save your BMI record.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Could not save. Ensure weight, height, and age are valid.")

    def view_history(self):
        # MODIFIED: Populates the Treeview in the main window
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Missing Name", "Please enter a name to view history.")
            return

        # Clear existing items in the tree
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        records = get_user_history(name)
        if not records:
            messagebox.showinfo("No History", f"No records found for '{name}'.")
            return

        # Insert new records
        for record in records:
            self.history_tree.insert("", END, values=record)

    def show_trends(self):
        # This function remains largely the same
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Missing Name", "Please enter a name to show trends.")
            return
        records = get_user_history(name)
        if len(records) < 2:
            messagebox.showinfo("Not Enough Data", "At least two records are needed to plot a trend.")
            return
        plot_bmi_trend(records)

def run_gui():
    root = tb.Window(themename="superhero")
    app = BMIGui(root)
    root.mainloop()

if __name__ == '__main__':
    run_gui()