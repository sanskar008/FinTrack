import sqlite3

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS expenses")
    c.execute('''CREATE TABLE expenses
                 (id INTEGER PRIMARY KEY, amount REAL, category TEXT, subcategory TEXT, description TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS budget
                 (id INTEGER PRIMARY KEY, amount REAL)''')
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

def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def set_budget(amount):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM budget")
    c.execute("INSERT INTO budget (amount) VALUES (?)", (amount,))
    conn.commit()
    conn.close()

def get_budget():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT amount FROM budget LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

if __name__ == "__main__":
    init_db()