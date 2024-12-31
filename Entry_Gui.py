import tkinter as tk
import customtkinter as ctk

entry_window = ctk.CTk()
entry_window.title("Transaction Entry")
entry_window.geometry("400x300")

# Create labels and entry fields
Entry_Frame = ctk.CTkFrame(entry_window)

ctk.CTkLabel(entry_window, text="Date (mm/dd/yyyy):").grid(row=4, column=1, padx=10, pady=10)
date_entry = ctk.CTkEntry(entry_window, width=30)
date_entry.grid(row=0, column=1, padx=10, pady=10)

ctk.CTkLabel(entry_window, text="Description:").grid(row=1, column=0, padx=10, pady=10)
description_entry = ctk.CTkEntry(entry_window, width=30)
description_entry.grid(row=1, column=1, padx=10, pady=10)

ctk.CTkLabel(entry_window, text="Price:").grid(row=2, column=0, padx=10, pady=10)
price_entry = ctk.CTkEntry(entry_window, width=30)
price_entry.grid(row=2, column=1, padx=10, pady=10)
ctk.CTkLabel(entry_window, text="Category:").grid(row=3, column=0, padx=10, pady=10)
category_entry = ctk.CTkEntry(entry_window, width=30)
category_entry.grid(row=3, column=1, padx=10, pady=10)

# Create buttons
save_button = tk.Button(entry_window, text="Save Transaction")
save_button.grid(row=4, column=0, columnspan=2, pady=20)

# Start the Tkinter event loop
entry_window.mainloop()