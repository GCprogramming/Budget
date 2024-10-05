import sqlite3

def create_unified_db(year):
    try:
        db_name = f'Budget_{year}.db'
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Create the unified Transactions table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                Date TEXT NOT NULL, 
                Name TEXT NOT NULL, 
                Price FLOAT NOT NULL, 
                Category TEXT NOT NULL,
                Month TEXT NOT NULL,
                Year INTEGER NOT NULL,
                Account TEXT, 
                UNIQUE (Date, Name, Price, Category, Month, Year)
            )
        ''')

        # Create the Categories table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL,
                category_type TEXT NOT NULL -- Income, Expense, or Saving
            )
        ''')

        # Create the BankAccounts table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS BankAccounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_name TEXT NOT NULL,
                bank_name TEXT,
                account_number TEXT,
                account_type TEXT, -- Savings, Checking, etc.
                balance FLOAT NOT NULL
            )
        ''')

        # Create the BudgetAllocation table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS BudgetAllocation (
                allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                projected_budget FLOAT NOT NULL,
                actual_budget FLOAT,
                month_year TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES Categories(category_id)
            )
        ''')

        # Create the RecurringPayments table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS RecurringPayments (
                recurring_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                projected_amount FLOAT NOT NULL,
                actual_amount FLOAT,
                description TEXT,
                FOREIGN KEY (account_id) REFERENCES BankAccounts(account_id),
                FOREIGN KEY (category_id) REFERENCES Categories(category_id)
            )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
    print (4)
    return db_name

# Example usage
db_name = create_unified_db(2024)
