# =====================================================
# CUSTOMER SEGMENTATION DASHBOARD
# Python + Pandas + Matplotlib + Tkinter + Seaborn
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import messagebox, filedialog
import os

# Set plot aesthetics
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (8,5)

# =====================================================
# GLOBAL VARIABLES
# =====================================================
df = None  # Dataframe
high_value = None  # High value customers

# =====================================================
# HELPER FUNCTIONS FOR PLOTTING
# =====================================================
def plot_bar(series, title='', color='skyblue', rotate=0):
    counts = series.value_counts()
    plt.bar(counts.index.astype(str), counts.values, color=color)
    plt.title(title)
    plt.xlabel(series.name)
    plt.ylabel('Count')
    plt.xticks(rotation=rotate)
    plt.tight_layout()
    plt.show()

def plot_hist(series, bins=10, color='skyblue', title='', xlabel=''):
    plt.hist(series, bins=bins, color=color, edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

# =====================================================
# FILE LOADING FUNCTION
# =====================================================
def load_file():
    global df
    file_path = filedialog.askopenfilename(
        title="Select Customer File",
        filetypes=[("CSV & Excel Files", "*.csv *.xlsx *.xls"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.csv':
                df = pd.read_csv(file_path)
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file format!")
                return

            # Handle missing values
            df['Profession'] = df['Profession'].fillna('Unknown')
            df['Work_Experience'] = df['Work_Experience'].fillna(df['Work_Experience'].median())

            # Prepare age groups
            bins = [18, 30, 45, 60, 100]
            labels = ['Young', 'Adult', 'Mid-Age', 'Senior']
            df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

            messagebox.showinfo("Success", "File Loaded Successfully!")
            status_label.config(text=f"File Loaded: {os.path.basename(file_path)}", fg="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# =====================================================
# VISUALIZATION FUNCTIONS
# =====================================================
def gender_distribution():
    if df is not None:
        plot_bar(df['Gender'], title='Customer Distribution by Gender', color='lightcoral')

def age_distribution():
    if df is not None:
        plot_hist(df['Age'], bins=12, color='skyblue', title='Age Distribution', xlabel='Age')

def spending_distribution():
    if df is not None:
        plot_bar(df['Spending_Score'], title='Spending Score Distribution', color='orange')

def profession_vs_spending():
    if df is not None:
        prof_sp = pd.crosstab(df['Profession'], df['Spending_Score'])
        prof_sp = prof_sp.sort_values('High', ascending=False)
        prof_sp.plot(kind='bar', stacked=True, figsize=(10,6))
        plt.title("Profession vs Spending Score (Stacked)")
        plt.xlabel("Profession")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def age_group_distribution():
    if df is not None:
        plot_bar(df['Age_Group'], title='Customer Segmentation by Age Group', color='green')

def family_size_distribution():
    if df is not None:
        plot_hist(df['Family_Size'], bins=5, color='purple', title='Family Size Distribution', xlabel='Family Size')

def high_value_customers():
    global high_value
    if df is not None:
        high_value = df[(df['Spending_Score'] == 'High') & (df['Work_Experience'] > 5)]
        messagebox.showinfo("High Value Customers", f"Total High Value Customers: {len(high_value)}")

def summary_insights():
    if df is not None:
        hv_count = len(df[(df['Spending_Score'] == 'High') & (df['Work_Experience'] > 5)])
        summary = pd.DataFrame({
            "Metric": [
                "Total Customers",
                "Most Common Spending Category",
                "Most Common Profession",
                "Average Age",
                "Average Work Experience",
                "High Value Customers"
            ],
            "Value": [
                len(df),
                df['Spending_Score'].mode()[0],
                df['Profession'].mode()[0],
                round(df['Age'].mean(), 2),
                round(df['Work_Experience'].mean(), 2),
                hv_count
            ]
        })
        messagebox.showinfo("Summary Insights", summary.to_string(index=False))

# =====================================================
# EXPORT FUNCTION (Option B)
# =====================================================
def export_results():
    global df, high_value
    if df is not None:
        folder = filedialog.askdirectory(title="Select Folder to Save Files")
        if folder:
            # Save cleaned dataset
            cleaned_path = os.path.join(folder, "Customer_Segmentation_Cleaned.csv")
            df.to_csv(cleaned_path, index=False)

            # Save high-value customers
            if high_value is None:
                high_val = df[(df['Spending_Score'] == 'High') & (df['Work_Experience'] > 5)]
            else:
                high_val = high_value
            high_value_path = os.path.join(folder, "High_Value_Customers.csv")
            high_val.to_csv(high_value_path, index=False)

            messagebox.showinfo(
                "Export Complete",
                f"Files exported successfully to:\n{folder}\n\n"
                f"1. {cleaned_path}\n2. {high_value_path}"
            )

# =====================================================
# TKINTER GUI
# =====================================================
root = tk.Tk()
root.title("Customer Segmentation Dashboard")
root.geometry("520x700")
root.configure(bg="#2c3e50")  # Dark background

# Title
title = tk.Label(root, text="Customer Segmentation Dashboard",
                 font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
title.pack(pady=20)

# Button style
button_bg = "#3498db"  # Blue
button_fg = "white"

# Buttons
load_btn = tk.Button(root, text="Load File", width=30, height=2, bg=button_bg, fg=button_fg, command=load_file)
load_btn.pack(pady=10)

btn1 = tk.Button(root, text="Gender Distribution", width=30, height=2, bg=button_bg, fg=button_fg, command=gender_distribution)
btn1.pack(pady=8)

btn2 = tk.Button(root, text="Age Distribution", width=30, height=2, bg=button_bg, fg=button_fg, command=age_distribution)
btn2.pack(pady=8)

btn3 = tk.Button(root, text="Spending Distribution", width=30, height=2, bg=button_bg, fg=button_fg, command=spending_distribution)
btn3.pack(pady=8)

btn4 = tk.Button(root, text="Profession vs Spending", width=30, height=2, bg=button_bg, fg=button_fg, command=profession_vs_spending)
btn4.pack(pady=8)

btn5 = tk.Button(root, text="Age Group Distribution", width=30, height=2, bg=button_bg, fg=button_fg, command=age_group_distribution)
btn5.pack(pady=8)

btn6 = tk.Button(root, text="Family Size Distribution", width=30, height=2, bg=button_bg, fg=button_fg, command=family_size_distribution)
btn6.pack(pady=8)

btn7 = tk.Button(root, text="High Value Customers", width=30, height=2, bg=button_bg, fg=button_fg, command=high_value_customers)
btn7.pack(pady=8)

btn8 = tk.Button(root, text="Summary Insights", width=30, height=2, bg=button_bg, fg=button_fg, command=summary_insights)
btn8.pack(pady=8)

btn9 = tk.Button(root, text="Export Results", width=30, height=2, bg="#27ae60", fg="white", command=export_results)  # Green button
btn9.pack(pady=15)

# Status label
status_label = tk.Label(root, text="No File Loaded", bg="#2c3e50", fg="red", font=("Arial", 12))
status_label.pack(pady=10)

root.mainloop()
