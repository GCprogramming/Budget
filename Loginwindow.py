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