import sqlite3

def add_category(db_name, category_name, category_type):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Categories (category_name, category_type) 
            VALUES (?, ?)
        ''', (category_name, category_type))
        conn.commit()
        print(f"Category '{category_name}' added successfully.")
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

def delete_category(db_name, category_id):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        
        # Delete the category from the Categories table
        cur.execute('''
            DELETE FROM Categories WHERE category_id = ?
        ''', (category_id,))
        
        conn.commit()
        print(f"Category with ID '{category_id}' deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()