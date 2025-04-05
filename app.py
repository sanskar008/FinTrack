from flask import Flask, render_template, request
from database import init_db, add_expense, get_expenses
from ml_model import analyze_spending

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        subcategory = request.form['subcategory']
        description = request.form['description']
        date = request.form['date']
        add_expense(amount, category, subcategory, description, date)
    
    expenses = get_expenses()
    notifications = analyze_spending(expenses)
    return render_template('index.html', expenses=expenses, notifications=notifications)

if __name__ == '__main__':
    init_db()  # Recreate DB with new schema
    app.run(debug=True)