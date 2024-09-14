import os
print(os.getcwd())
import sqlite3
from tkinter import ttk
import calendar
from tkinter import simpledialog
import customtkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import pdfplumber
import re
from datetime import datetime


import loginwindow as lw


#Global Time Variables 

        
        
now = datetime.now() 
current_year = datetime.now().year
current_month = now.month
day = now.strftime('%m/%d/%y')

MIN_YEAR = 2020
MAX_YEAR = 2100
def get_month(month):
    if 1 <= month <= 12:
        return calendar.month_name[month]
    else:
        return None
month = get_month(current_month)
year = current_year #int(input('Input Year: '))

#Create Database
def create_yearly_db(year): 
    try:
        db_name = f'Transactions_{year}.db'
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        months = ["January", "February", "March", 
                "April", "May", "June","July", "August", 
                "September", "October", "November","December"]
            
        for month in months:    
            table_name = f'{month} {year}'        
            cur.execute(f'''
                    CREATE TABLE IF NOT EXISTS "{table_name}" (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                        Date TEXT NOT NULL, 
                        Name TEXT NOT NULL, 
                        Price FLOAT NOT NULL, 
                        Category TEXT NOT NULL,
                        UNIQUE (Date, Name, Price, Category)
                    )
                ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    conn.close()
    return db_name
db_name = create_yearly_db(current_year)



  
    
def get_all_categories(month, year, conn):
    cur = conn.cursor()
    table_name = f"{month} {year}"
    cur.execute(f'SELECT DISTINCT Category FROM "{table_name}"')
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories

def close_window(window):
    window.destroy()
  

    
def menu_window():
    def on_treeview_select(event):
        selected_item = treeview.selection()
        if selected_item:
            delete_button.configure(state=tk.NORMAL)
            update_button.configure(state=tk.NORMAL)
    def create_treeview(display_frame):    
        
        treeview = ttk.Treeview(display_frame,columns=('name','price','category'),
                                padding='3m',displaycolumns='#all',height=30,)
        treeview.column('#0', stretch=tk.NO)
        treeview.heading('#0',text='Date',anchor=tk.CENTER, )
        treeview.heading('name',text='Name',anchor=tk.CENTER, command=lambda: sort_treeview(treeview, 'name', False))
        treeview.heading('price',text='price',anchor=tk.CENTER, command=lambda: sort_treeview(treeview, 'price', False))
        treeview.heading('category',text='Category',anchor=tk.CENTER, command=lambda: sort_treeview(treeview, 'category', False)) 
        treeview.bind('<<TreeviewSelect>>', on_treeview_select)
        treeview.pack(expand='True', fill= 'both')
        
        return treeview
    menu_window = tk.CTk()
    menu_window.title('Transaction Manager')
    tk.set_appearance_mode('dark')
# Fonts
    title_font1 = tk.CTkFont(family="Comic Sans MS", size=15, weight="bold")
    text_font1 = tk.CTkFont(family="Courier New", size=12, weight="normal")
    button_font1 = tk.CTkFont(family="Times", size=10, weight="normal")
    custom_font3 = tk.CTkFont(family="Noto Sans", size=14, weight="bold")
#Frames
    main_frame = tk.CTkFrame(menu_window,)   
    main_frame.pack(expand= True, fill='x')
    menu_frame = tk.CTkFrame(main_frame,)
    menu_frame.pack(fill='y',side='left')
    balance_frame = tk.CTkFrame(main_frame,)
    balance_frame.pack(fill='y',side='right')
    user_frame = tk.CTkFrame(main_frame,height= 100)
    user_frame.pack(side='top',fill='both')
    date_frame = tk.CTkFrame(user_frame,width=100, height=20)
    date_frame.grid(row=0,column=0,columnspan=5,padx=5, )
    input_frame = tk.CTkFrame(user_frame,width=100, height=20)
    input_frame.grid(row=1,column=0,columnspan=2,rowspan=3)
    input_frame2=tk.CTkFrame(user_frame,width=500, height=20) 
    input_frame2.grid(column=2,row=1,)
    filter_frame = tk.CTkFrame(input_frame2)
    upload_frame = tk.CTkFrame(input_frame2)
    display_frame = tk.CTkFrame(main_frame,height= 20)  
    display_frame.pack(side ='bottom')
    treeview = create_treeview(display_frame)
    
    
#MENU Frame 
    menu_option = tk.IntVar(value=1)
    #Radio Button Options 
    search_option = tk.CTkRadioButton(menu_frame, text = ' FILTER | DELETE',
                            variable= menu_option, value=1,font=button_font1,
                            command=lambda: change_frame_widgets())
    search_option.grid(row=0,column=0,ipadx=7,ipady=7)
  
    upload_option = tk.CTkRadioButton(menu_frame, text='STATEMENT| FILE\n UPLOAD', 
                            variable= menu_option, value =2,font=button_font1,
                            command=lambda: change_frame_widgets())
    upload_option.grid(row=3,column=0,ipadx=7,ipady=7)
    
#Balance Frame 
    m=f'{month} {year}'#get function to return m 
    
    monthly_breakdown_label  = tk.CTkLabel(balance_frame, text= f'{m}\nBreakdown',font=title_font1)
    monthly_breakdown_label.grid(row=5,column=0,padx=7, ipady=3 ,pady=7,)
    def update_monthly_breakdown_label(month, year):
        # Format the month and year into the desired format
        m = f'{month} {year}'
        # Update the label text
        monthly_breakdown_label.configure(text=f'{m}\nBreakdown')
    
    
    
    def get_column_values(treeview, column_name):
        column_index = treeview["columns"].index(column_name)
        values = []
        for item in treeview.get_children():
            try:
                value = treeview.item(item, 'values')[column_index]
                value = float(value)
                values.append(value)
            except ValueError:
                pass
        return values
    #Income    
    def income_total(treeview): # gets monthly total 
        prices = get_column_values(treeview, 'price')  # Column for prices
        total = sum(x for x in prices if x > 0)  # Sum positive values (income)
        return f'{total:.2f}'
    x = income_total(treeview)
    income_label = tk.CTkLabel(balance_frame, text= f'Gross Income\n{x}',font=text_font1)
    income_label.grid(row=6,column=0,padx=7, ipady=3 ,pady=7)    
    
    
    #Expense    
    def expense_total(treeview): # gets monthly total 
       prices = get_column_values(treeview, 'price')  # Column for prices
       total = sum(x for x in prices if x < 0)  # Sum negative values (expenses)
       return f'{abs(total):.2f}'
    x = expense_total(treeview)
    expense_label  = tk.CTkLabel(balance_frame, text= f'Total Expense\n{x}',font=text_font1)
    expense_label.grid(row=7,column=0,padx=7, ipady=3 ,pady=7)   
    
    
    
    
    
    #NET        
    def monthly_net(treeview): # gets monthly total 
        values = get_column_values(treeview, 'price')
        return sum(values)
    x = monthly_net(treeview)
    net_label = tk.CTkLabel(balance_frame, text= f'Net\n{x:.2f}',font=text_font1)
    net_label.grid(row=8,column=0,padx=7, ipady=3 ,pady=7)

    category_label  = tk.CTkLabel(balance_frame, text= 'Category\nSummary',font=title_font1)
    category_label.grid(row=9,column=0,padx=7, ipady=3 ,pady=7,)
    
    
   
    def get_category_total(treeview, category_name):#Function to get specific cat
        prices = get_column_values(treeview, 'price')  # Column index for price
        categories = [treeview.item(item, 'values')[2] for item in treeview.get_children()]  # Column index for category
        total = sum(float(price) for price, category in zip(prices, categories) if category == category_name)
        return total
    
    def category_percent(category_total, treeview):
        total = sum(get_column_values(treeview, 'price'))  # Total from all expenses
        if total == 0:
            return "0"
        percent = abs((category_total / total) * 100)
        return f"{round(percent)}"

    def update_category_labels(treeview, category_labels):
        income_value = income_total(treeview)
        inv = float(income_value)
        expense_value = expense_total(treeview)
        exv = float(expense_value)
        net_value = f'{(inv-exv):.2f}'
        net_label.configure(text=f"Net\n{net_value}")

        income_label.configure(text=f"Gross Income\n{income_value}")
        expense_label.configure(text=f"Total Expense\n{expense_value}")
        
        categories = ['Savings', 'Investment', 'Debt(Paid)','Debt(Received)', 'Transport/Gas',
                      'Rent', 'Groceries', 'Personal', 'Education','Entertainment', 'Misc']
        for category in categories:
            category_total_amount = get_category_total(treeview, category)
            percent = category_percent(category_total_amount, treeview)
            category_labels[category].configure(text=f'{category}\n{category_total_amount:.2f}  %{percent}')
                               
    def setup_labels(frame):
        categories = ['Savings', 'Investment', 'Debt(Paid)','Debt(Received)', 'Transport/Gas',
                      'Rent', 'Groceries', 'Personal', 'Education','Entertainment', 'Misc']
        category_labels = {}
        for idx, category in enumerate(categories):
            label = tk.CTkLabel(frame, text=f'{category}\n0.00  %0', font=('Arial', 12))
            label.grid(row=13 + idx, column=0, padx=7, ipady=3, pady=7)
            category_labels[category] = label
        return category_labels   
    category_labels = setup_labels(balance_frame)  
# User Frame      
    #Date Frame
    month_entry = tk.CTkEntry(date_frame,width=100, justify='center') 
    month_entry.grid( row=0,column=0,)
    month_entry.insert(0, month) 
    
    year_entry = tk.CTkEntry(date_frame, width= 50, justify='center',)
    year_entry.grid(row=0,column=1,padx=10,)
    year_entry.insert(0,year)
    
    def show_calendar(event=None):
        current_month = month_entry.get()
        current_year = year_entry.get()
        if current_month.isdigit():
            current_month = int(current_month)
        else:
            current_month = list(calendar.month_name).index(current_month)
        
        current_year = int(current_year)
        selected_date = None

    
        
        def previous_month(): 
            nonlocal current_month, current_year
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1
            build_calendar()
        def next_month():
            global current_month, current_year
            current_month += 1
            if current_month == 13:
                current_month = 1
                current_year += 1
            build_calendar()
    
        def select_date(day):
            nonlocal selected_date
            selected_date = datetime(current_year, current_month, day)
            top.destroy()
            if selected_date:
                on_date_selected(selected_date)

    
        def build_calendar():
            # Clear previous calendar widgets
            for widget in top.winfo_children():
                widget.destroy()
    
            # Set the month name
            month_name = calendar.month_name[current_month]
    
            # Create navigation buttons for the calendar
            prev_button = tk.CTkButton(top, text="<", command=previous_month)
            prev_button.grid(row=0, column=0)
    
            # Display the current month and year
            label = tk.CTkLabel(top, text=f"{month_name} {current_year}")
            label.grid(row=0, column=1, columnspan=5)
    
            next_button = tk.CTkButton(top, text=">", command=next_month)
            next_button.grid(row=0, column=6)
    
            # Display day labels
            day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for i, day_label in enumerate(day_labels):
                label = tk.CTkLabel(top, text=day_label)
                label.grid(row=1, column=i)
    
            # Display days of the month
            days = calendar.Calendar().monthdayscalendar(current_year, current_month)
            for i, week in enumerate(days, start=2):
                for j, day in enumerate(week):
                    if day != 0:
                        btn = tk.CTkButton(top, text=day, command=lambda d=day: select_date(d))
                        btn.grid(row=i, column=j)
                        
                        

    # Create a new top-level window for the calendar
        top = tk.CTkToplevel()
        top.title("Calendar")
        top.lift()
        top.focus_set()
        top.grab_set()
    
        # Build the initial calendar view
        build_calendar()
    
        # Wait for the calendar window to close
        top.wait_window()

    # If a date was selected, show label of date selected and update treeview 
        if selected_date:
            on_date_selected(selected_date)
    date_button = tk.CTkButton(date_frame,text='Pick a Date',font=text_font1, command=show_calendar)
    date_button.grid(row=0,column=2,padx=5, pady=1,)
    def update_calendar():
        global year, month
        year = int(year_entry.get())
        month = int(month_entry.get())
        show_calendar()

    #INPUT Frame 
    date_label = tk.CTkLabel(input_frame,text= (f'Date: {day}'),font=title_font1)
    date_label.grid(row=1,column=0, columnspan= 2)
    
    name_label = tk.CTkLabel(input_frame, text='Transaction Name:',font=title_font1)
    name_label.grid(row=2,column=0,)
    
    name_entry = tk.CTkEntry(input_frame, width=250, height=25)
    name_entry.grid(row=2,column=1,columnspan=3)
    
    price_label = tk.CTkLabel(input_frame, text='Amount($):',font=title_font1)
    price_label.grid(row=3,column=0,)
    
    price_entry = tk.CTkEntry(input_frame, width= 250, height=25)   
    price_entry.grid(row=3,column=1,columnspan=3)
    
    category_label = tk.CTkLabel(input_frame, text='Seclect Category:',font=title_font1)
    category_label.grid(row=4,column=0)
   
    n = tk.StringVar()
    category_combobox  = ttk.Combobox(input_frame, textvariable = n, width=18) 
      
    category_combobox ['values'] = sorted(['Rent','Groceries',"Savings",'Investment',
                               'Transport/Gas','Entertainment', 'Misc', 
                               'Education','Debt(Paid)','Debt(Recived)',
                               'Personal','Insurance', 'Entertainment']) 
    category_combobox .grid( row=4,column=1,padx=7, ipady=3 ,pady=7,)
    
    category_combobox .current()
    def close_menu_window():
        close_window(menu_window)        
    Exit_button = tk.CTkButton(input_frame, text = 'Exit',width=50,height=10,
                                 font=button_font1,command= close_menu_window)
    Exit_button.grid(row=4,column=3,ipadx=7,ipady=7) 
    


#Input Frame 2/Changable 
    
    
    #Filter Frame
    search_label = tk.CTkLabel(filter_frame, text='Search Name:',font=title_font1)
    search_label.grid(row=0,column=0,padx=7, ipady=3 ,pady=7,)
    search_entry = tk.CTkEntry(filter_frame,width= 120, height=20)
    search_entry.grid(row=0,column=1,ipadx=2, ipady=2, padx=5, pady=5)

    search_button = tk.CTkButton(filter_frame,text ='Search',width=50,height=10,
                                 font=button_font1,)
    search_button.grid(row=0,column=2,ipadx=7,ipady=7)    
    
    filter_category_label = tk.CTkLabel(filter_frame, text='Filter Category:',
                                        font=title_font1)
    filter_category_label.grid(row=1,column=0,padx=7, ipady=3 ,pady=7)

        #Filter Scrollbox    
    n1 = tk.StringVar()
    Filter = ttk.Combobox(filter_frame, textvariable = n1,width=14,) 
      
    Filter['values'] = sorted([ 'Rent','Groceries',"Savings", 'Investment',
                               'Transport/Gas','Entertainment', 'Misc', 
                               'Education','Debt(Paid)','Debt(Recived)',
                               'Personal','Insurance', 'Entertainment']) 
    Filter.grid( row=1,column=1, ipadx=7, ipady=7 ,)
    Filter.current()
      
    filter_button = tk.CTkButton(filter_frame, text = 'Filter',width=50,height=10,
                                 font=button_font1,)
    filter_button.grid(row=1,column=2,ipadx=7,ipady=7,) 
    def update_treeview_item():
        if treeview.selection():
            delete_button.configure(state=tk.NORMAL)
            update_button.configure(state=tk.NORMAL)
           
        else:
            print("No items selected")
            update_button.configure(state=tk.DISABLED)
            delete_button.configure(state=tk.DISABLED)
            
        year = year_entry.get()
        month = month_entry.get()
        db_name = f'Transactions_{year}.db'
        month_name = f"{month} {year}"
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        selected_items = treeview.selection()
        if not selected_items:
         print("No items selected for update")
         return
        print('Processing updates...')
        for selected_item in selected_items:
            # Retrieve current values from the Treeview
            current_values = treeview.item(selected_item, 'values')
            date_value = treeview.item(selected_item, 'text')  # Date from Treeview
            month_name = f"{month} {year}"
            print(f"Current Values: {current_values}")
            print(f"Date Value: {date_value}")
        
            # Assuming the ID is stored in the Treeview (e.g., as the first or last value)
            # Adjust the index as needed based on how you store the ID in Treeview
            transaction_id = treeview.item(selected_item, 'text')  # Example: assuming the ID is the text identifier
            print(f"Transaction ID: {transaction_id}")
            # Get new values or keep the current ones if fields are empty
            new_name = name_entry.get() if name_entry.get() else current_values[0]
            new_price1 = price_entry.get() if price_entry.get() else current_values[1]
            new_price= float(new_price1)
            new_category = category_combobox.get() if category_combobox.get() else current_values[2]
            print(f"New Values - Name: {new_name}, Price: {new_price}, Category: {new_category}")
            # Update the Treeview with new values
            treeview.item(selected_item, values=(new_name, new_price, new_category))
            print("Treeview updated with new values.")
            # Build the UPDATE SQL statement
            updates = []
            params = []
        
            if new_name != current_values[0]:
                updates.append("Name = ?")
                params.append(new_name)
            if new_price != current_values[1]:
                updates.append("Price = ?")
                params.append(new_price)
            if new_category != current_values[2]:
                updates.append("Category = ?")
                params.append(new_category)
        
            # Add the ID to uniquely identify the row in the database
            if updates:
                updates_str = ", ".join(updates)
                params.append(transaction_id)  # Add ID to the parameter list
                print(f"Executing SQL: UPDATE \"{month_name}\" SET {updates_str} WHERE ID = ?")
                print(f"Parameters: {params}")
                try:
                    cur.execute(f'''
                        UPDATE "{month_name}" SET {updates_str} 
                        WHERE ID = ?
                    ''', params)
                    conn.commit()
                    print("Database updated successfully.")
                except sqlite3.IntegrityError as e:
                    print(f"Failed to update due to integrity constraint: {e}")
                except sqlite3.Error as e:
                                print(f"SQL Error: {e}")
        # Clear input fields
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        category_combobox.delete(0, tk.END)
        
        # Close the database connection
        conn.close()
            
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        category_combobox .delete(0, tk.END)  
    update_button = tk.CTkButton(filter_frame, text = 'Update',width=50,height=10,
                                     font=button_font1,command=update_treeview_item)
    update_button.grid(row=2,column=1,ipadx=7,ipady=7, padx=1)
    update_button.configure(state=tk.DISABLED)
    
    def delete_transaction():
        now = datetime.now()
        current_month = now.month
        db_name = f'Transactions_{year}.db'
        month = get_month(current_month)
        month_name = f"{month} {year}"
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        
        selected_item = treeview.selection()  # Get selected item
        if selected_item:  # Ensure something is selected
            item_values = treeview.item(selected_item)['values']
            
            if len(item_values) == 3:  # Adjust based on the actual number of columns
                # Extract values based on current column indices
                transaction_name = item_values[0]  # 'Name' column
                transaction_price = float(item_values[1])  # 'price' column
                transaction_category = item_values[2]  # 'Category' column
               
                # Delete the selected item from the Treeview
                treeview.delete(selected_item)
                
                # Execute the SQL DELETE statement
                sql_query = f'''DELETE FROM "{month_name}" WHERE name = ? AND price = ? AND category = ?'''
                
                print(f"{transaction_name} ${transaction_price}, {transaction_category}")
                
                cur.execute(sql_query, (transaction_name, transaction_price, transaction_category))
                conn.commit()
                
                # Check if any rows were affected
                if cur.rowcount > 0:
                    print('Deleted successfully')
                else:
                    print('No rows deleted, check data integrity')
                
                # Disable the delete button after deletion
                delete_button.configure(state=tk.DISABLED)
            else:
                messagebox.showinfo("Delete", "The selected transaction does not have the expected number of columns.")
        else:
            messagebox.showinfo("Delete", "No transaction selected")
        
        # Close the database connection
        conn.close()
    delete_button = tk.CTkButton(filter_frame, text = 'Delete',width=50,height=10,
                                 font=button_font1,command=delete_transaction)
    delete_button.grid(row=2,column=2,ipadx=7,ipady=7, padx=1)
    delete_button.configure(state=tk.DISABLED)
   
#Upload Frame
    def extract_pdf_data(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                all_text += page_text
        return all_text
    def extract_data(text):
        deposit_section = re.search(
            r"Deposits and other additions\n(.*?)(?=\n(?:Withdrawals and other subtractions|Total deposits and other additions|$))",
            text, re.DOTALL)
        withdrawal_section = re.search(
            r"Withdrawals and other subtractions\n(.*?)(?=\n(?:Total withdrawals and other subtractions|Total deposits and other additions|$))",
            text, re.DOTALL)
        
        deposits  = deposit_section.group(1) if deposit_section else ""
        withdrawals  = withdrawal_section.group(1) if withdrawal_section else ""
        
    
        
        def get_category(description):
                description = description.lower()
                if any(keyword in description for keyword in[ "zelle ","atm",]):
                    return "Personal"
                elif any(store in description for store in ["walmart", "wm supercenter", "wal-mart"]):
                    return "Groceries"
                elif any(store in description for store in ["racetrack", "quicktrip", "7-eleven", "abc wrecker", "qt", "vehreg"]):
                    return "Transportation"
                elif any(store in description for store in ["payroll"]):
                    return "Payroll"
                elif any(keyword in description for keyword in ["park place", "simple bills", "rent", "simplebills"]):
                    return "Rent"
                elif "discover" in description:
                    return "Debt Paid"
                elif "schwab brokerage" in description:
                    return "Investment"
                else:
                    return "Misc"
    
    #Bank upload processors 
    
        def parse_deposits(section):
            transactions = []
            lines = section.splitlines()
            for line in lines:
                line = line.strip()
                if not line or "Date Description Amount" in line or "Total" in line:
                    continue
                # Adjust the regex pattern to match the expected deposit line format
                match = re.match(
                    r"(\d{2}/\d{2}/\d{2})\s+(.*?)\s+([\d,]+\.\d{2})$", line
                )
                if match:
                    date, description, amount = match.groups()
                    description = description[:100]
                    # Ensure amount is formatted correctly
                    amount = amount.replace(',', '')  # Remove commas from amount
                    category = get_category(description)
                    transactions.append((date, description, category, amount))
                else:
                    print(f"Deposit line not matched: {line}")  # Debugging print statement
            return transactions
        
        def parse_withdrawals(section):
            transactions = []
            lines = section.splitlines()
            for line in lines:
                line = line.strip()
                if not line or "Date Description price" in line or "Total" in line:
                    continue
                match = re.match(r"(\d{2}/\d{2}/\d{2})\s+(.*?)(?:\s+(-?\$?\d+\.\d{2}))?$", line)
                if match:
                    date, description, price = match.groups()
                    description = description[:100]  # Increase truncation length
                    price = price.replace('$', '').replace(',', '') if price else "0.0"  # Clean up price
                    category = get_category(description)
                    transactions.append((date, description, category, price))
            return transactions
        
        deposit_transactions = parse_deposits(deposits)
        withdrawal_transactions = parse_withdrawals(withdrawals)
        
        return deposit_transactions, withdrawal_transactions
    def insert_into_treeview(treeview, income_transactions, expense_transactions):
        clear_treeview(treeview)
        unique_counter = 0
        
        for date, description, category, price in income_transactions:
            unique_id = f"{date}{description}{unique_counter}"
            treeview.insert("", tk.END, iid=unique_id, text=date, values=(description, price, category))
            unique_counter += 1
        for date, description, category, price in expense_transactions:
            unique_id = f"{date}{description}{unique_counter}"
            treeview.insert("", tk.END, iid=unique_id, text=date, values=(description, price, category))
            unique_counter += 1
 
    # File Type 
    file_type_var = tk.StringVar(value="PDF")      
    pdf_rb = tk.CTkRadioButton(upload_frame, text="PDF", variable=file_type_var, value="PDF")
    pdf_rb.grid(column=0, row=0)
    
    csv_rb = tk.CTkRadioButton(upload_frame, text="CSV", variable=file_type_var, value="CSV")
    csv_rb.grid(column=0, row=1)
   
                                                    
    def clear_treeview(treeview):
        for item in treeview.get_children():
                treeview.delete(item)
    def upload_file():
        file_path = file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("CSV files", "*.csv")])  # Example path
        if file_path:
            text = extract_pdf_data(file_path)
            deposits, withdrawals = extract_data(text)
            insert_into_treeview(treeview, deposits, withdrawals)
        else:
            messagebox.showwarning("File Selection", "No file selected")
    upload_button = tk.CTkButton(upload_frame, text="Upload File", command= upload_file)
    upload_button.grid(column=1, row=1)
    
    banks = ["BOA", "Discover",]
    bank_combobox = tk.CTkComboBox(upload_frame, values=banks)
    bank_combobox.grid(column=1, row=0)
    bank_combobox.set("Select Bank")
    
    def save_to_db():
        try:
            db_connections = {}
    
            for child in treeview.get_children():
                # Extract data from the Treeview
                date = treeview.item(child, "text")  # Get date from the '#0' column (text field)
                values = treeview.item(child, "values")  # Get the remaining columns
                
                if values:
                    # Unpack the values (name, price, category)
                    name, price, category = values
                    try:
                        # Extract month and year from the transaction date
                        date_obj = datetime.strptime(date, '%m/%d/%y')
                        month = date_obj.strftime('%B')  # Extract full month name (e.g., 'July')
                        year = date_obj.strftime('%Y')   # Extract year (e.g., '2024')
    
                        # Ensure price is a float
                        price = float(price.replace('$', '').replace(',', ''))
    
                        # Determine the correct database and table based on the extracted year and month
                        db_name = f'Transactions_{year}.db'
                        table_name = f'{month} {year}'
    
                        # Connect to the database for the specific year if not already connected
                        if db_name not in db_connections:
                            db_connections[db_name] = sqlite3.connect(db_name)
                            print(f"Connected to database: {db_name}")
    
                        # Prepare the connection and cursor for the relevant year
                        conn = db_connections[db_name]
                        cur = conn.cursor()
    
                        # Create the table if it doesn't exist
                        cur.execute(f'''
                            CREATE TABLE IF NOT EXISTS "{table_name}" (
                                Date TEXT,
                                Name TEXT,
                                Price FLOAT,  
                                Category TEXT, 
                                UNIQUE (Date, Name, Price, Category)
                            )
                        ''')
    
                        cur.execute(f'''
                        INSERT OR IGNORE INTO "{table_name}" (Date, Name, Price, Category)
                        VALUES (?, ?, ?, ?)
                    ''', (date, name, price, category))

                        # Check for changes to determine if the record was inserted or ignored
                        if cur.rowcount == 0:
                            messagebox.showinfo("Info", f"Duplicate entry found: {date}, {name}, {price}, {category}. Skipping this entry.")
    
                    except ValueError as e:
                        messagebox.showwarning("Warning", f"Invalid date format or price in: {date}. Skipping this entry.")
                        continue
    
            # Commit all the changes and close each connection
            for db_name, conn in db_connections.items():
                conn.commit()
                print(f"Committed changes to database: {db_name}")
                conn.close()
    
            messagebox.showinfo("Success", "Transactions uploaded and saved to the database successfully!")
    
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    submit_button = tk.CTkButton(upload_frame, text="Submit", command=save_to_db)
    submit_button.grid(column=1, row=2)
    

    def change_frame_widgets():
        selected = menu_option.get()
        if selected == 1:
           upload_frame.grid_forget()
           filter_frame.grid(row=1, column=0, padx=10, pady=10)
        elif selected == 2:
            filter_frame.grid_forget()
            upload_frame.grid(row=1, column=0, padx=10, pady=10)
            


#Display Frame    
    #Sort Table
    def sort_treeview(treeview,column,reverse):
        for c in treeview["columns"]:
            treeview.heading(c, text=c.capitalize(), anchor=tk.CENTER)
        l = []
        for item in treeview.get_children(''):
            column_info = treeview.set(item,column)
            l.append((column_info,item))
        l.sort(reverse=reverse)
        
        for index, (_,item) in enumerate(l):
            treeview.move(item,'', index)
        treeview.heading(column, text=column.capitalize() + (" ▲" if not reverse else " ▼"), anchor=tk.CENTER)


   
    def search_for_transaction(x):
        found = False
        for child in treeview.get_children():
            if treeview.item(child, 'values')[0] == x:  # Checking the 'Name' column (index 0)
                found = True
                break
        if found:
           print ('Found') # stop duplication error, get and display 
        else:
            print('Apple does not exist')
            #create message box alert  
    
    def view_transaction():
        year = year_entry.get()
        month = month_entry.get()
        db_name = f'Transactions_{year}.db'
        month_name = f"{month} {year}"
        try:
           conn = sqlite3.connect(db_name)
           cur = conn.cursor()
           
           # Fetch the transaction data from the table
           cur.execute(f'SELECT Date, Name, Price, Category FROM "{month_name}"')
           rows = cur.fetchall()
               
           # Clear existing data in the Treeview
           for item in treeview.get_children():
               treeview.delete(item)
           
           # Insert data into Treeview
           for row in rows:
            date, name, price, category = row
            treeview.insert("", tk.END, text=date, values=(name, price, category))
           conn.close()
        except sqlite3.Error as e:
             messagebox.showerror("Error", f"An error occurred while accessing the database: {e}")
    
    def on_date_selected(selected_date):
        year = selected_date.year
        month = calendar.month_name[selected_date.month]
        year_entry.delete(0, tk.END)
        year_entry.insert(0, selected_date.year)
    
        month_entry.delete(0, tk.END)
        month_entry.insert(0, calendar.month_name[selected_date.month])
        update_monthly_breakdown_label(month, year)
        update_category_labels(treeview, category_labels)
        
        # Refresh the Treeview with transactions for the selected month
        view_transaction()
            
    
#Enter Button                    
    def add_transactrion():
        month = month_entry.get().strip()
        year = year_entry.get().strip()
        db_name = f'Transactions_{year}.db'
        month_name = f"{month} {year}"
        try:
            conn = sqlite3.connect(db_name)
            cur = conn.cursor()
            cur.execute(f'''
                CREATE TABLE IF NOT EXISTS "{month_name}" (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    Date TEXT NOT NULL, 
                    Name TEXT NOT NULL, 
                    Price FLOAT NOT NULL, 
                    Category TEXT NOT NULL,
                    UNIQUE (Date, Name, Price, Category)
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            conn.close()
            return
        try:
            date = day  # Ensure `day` is defined in your code or update accordingly
            name = name_entry.get() or 'N/A'
            price = price_entry.get() or '0.0'
            category = category_combobox .get() or 'Misc'
            
            # Insert into treeview
            treeview.insert("", tk.END, text=date, values=(name, price, category))
            
            # Insert into database
            cur.execute(f'''
                INSERT INTO "{month_name}" (Date, Name, price, Category)
                VALUES (?, ?, ?, ?)
            ''', (date, name, price, category))
            conn.commit()
            messagebox.showinfo("Success", f"{name} has been added to {month_name}.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()
            
        
    Enter_button = tk.CTkButton(input_frame, text = 'Enter',width=50,height=10,
                                 font=button_font1, command=add_transactrion)
    Enter_button.grid(row=4,column=2,ipadx=7,ipady=7,)   
    
    view_transaction()
    update_category_labels(treeview, category_labels)
    change_frame_widgets()
    menu_window.mainloop()
       

     
# User Login Window 
def login_window():
    login_window = tk.CTk()
    login_window.title('Budget Login Window' )
    login_window.geometry('300x200 ')
    
    
    main_frame = tk.CTkFrame(login_window,)
    main_frame.pack(expand=True, fill='both', padx=10, pady=10)
    
    main_frame.grid_rowconfigure(0, weight=0)
    main_frame.grid_rowconfigure(1, weight=0)
    main_frame.grid_columnconfigure(0, weight=0)
    main_frame.grid_columnconfigure(1, weight=1)
    
   
    #Labels 
   
    Username_label = tk.CTkLabel(main_frame,text='Username: ',
                              font=('Arial ',16))
    Username_label.grid(row=0, column=0, sticky='e', padx=10, pady=10)
    
    Username_entry = tk.CTkEntry(main_frame)
    Username_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
    
    Password_label = tk.CTkLabel(main_frame,text='Password: ',
                              font=('Arial ',16))
    Password_label.grid(row=1, column=0, sticky='e', padx=10, pady=10)
    
    Password_entry = tk.CTkEntry(main_frame, show='*')
    Password_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=10)
    
    login_button = tk.CTkButton(main_frame,text='Login',
                             command=lambda: login())
    login_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    #placement 
    
    
    
    
    
     #Quit Login Window
    def login_close_window():
        close_window(login_window)
    
    def login():
        username = ''
        password = ''
        if Username_entry.get() == username and Password_entry.get() == password:
            print('Valid Login')        
            login_close_window()
            menu_window()
        else:
            print('Invalid login ')
            messagebox.showinfo(title='Denied', message=' Invalid Login')
    
    login_window.mainloop()


def main():
    db_name = create_yearly_db(current_year)
    #login_window()
    menu_window()
    pass
main()
