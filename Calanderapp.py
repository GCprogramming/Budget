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