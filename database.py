import sqlite3

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    # Drop old table if it exists to avoid schema conflicts
    c.execute("DROP TABLE IF EXISTS expenses")
    c.execute('''CREATE TABLE expenses
                 (id INTEGER PRIMARY KEY, amount REAL, category TEXT, subcategory TEXT, description TEXT, date TEXT)''')
    conn.commit()
    conn.close()

def add_expense(amount, category, subcategory, description, date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category, subcategory, description, date) VALUES (?, ?, ?, ?, ?)",
              (amount, category, subcategory, description, date))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()
    return expenses

if __name__ == "__main__":
    init_db()