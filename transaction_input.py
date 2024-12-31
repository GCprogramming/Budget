import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import tkinter as tk
import customtkinter as ctk

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = '/Users/glenche/Desktop/Budget Code/budget-446303-cc80ce8d6ef3.json'

#credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
#client = gspread.authorize(credentials)
#transaction_sheet = client.open("2025 Budget").worksheet("Transactions")
#data = transaction_sheet.get_all_records()

date_width = 12
desc_width = 20
price_width = 10
category_width = 15

def add_transaction(Date, Description, Price, Category):
    Date = '01/01/2025' #datetime.now().strftime('%m/%d/%Y')
    Description = 'practice' #input("Enter the Description: ")
    Price = 0.0 #float(input("Enter the Price: "))
    Category = 'Free' #input("Enter the Category: ")
    
    with open("transactions.txt", "a") as file:
        row = (f"{Date:<12}{Description:<25}{Price:<10.2f}{Category:<15}\n")
        file.write(row)
        print("Transaction added.")

    
    
def create_header():    
    with open("transactions.txt", "w") as file:
    # Write header line
        header = (
            f"{'Date':<{date_width}}"
            f"{'Description':<{desc_width}}"
            f"{'Price':<{price_width}}"
            f"{'Category':<{category_width}}\n"
        )
        file.write(header)
        file.write("-" * (date_width + desc_width + price_width + category_width) + "\n")  # Separator
    



def add_row(Date,Description, Price, Category):
    transaction_sheet.append_row([Date,Description, Price, Category])



def save_transaction():
    Date = date_entry.get()
    Description = description_entry.get()
    Price = price_entry.get()
    Category = category_entry.get()
    
    add_transaction(Date, Description, Price, Category)
    
    date_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    
    print("Transaction saved.")

