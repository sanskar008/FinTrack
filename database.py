import sqlite3

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY, amount REAL, category TEXT, description TEXT, date TEXT)''')
    conn.commit()
    conn.close()

def add_expense(amount, category, description, date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
              (amount, category, description, date))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()
    return expenses

# Initialize the database
if __name__ == "__main__":
    init_db()