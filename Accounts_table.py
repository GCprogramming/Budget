import sqlite3
db_name = 'Budget_2024.db'

def add_bank_account(db_name, account_name, bank_name, account_number, account_type, balance):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO BankAccounts (account_name, bank_name, account_number, account_type, balance) 
            VALUES (?, ?, ?, ?, ?)
        ''', (account_name, bank_name, account_number, account_type, balance))
        conn.commit()
        print(f"Bank account '{account_name}' added successfully.")
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()
add_bank_account(db_name, "money rank", "Discover", "12345", "Credit", 0.00)
def delete_bank_account(db_name, account_id):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('''
            DELETE FROM BankAccounts WHERE account_id = ?
        ''', (account_id,))
        conn.commit()
        print(f"Bank account with ID '{account_id}' deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
a