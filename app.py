from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_expense, get_expenses, delete_expense, set_budget, get_budget
from ml_model import analyze_spending
from datetime import datetime, timedelta

app = Flask(__name__)

def get_weekly_summary(expenses):
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    weekly_expenses = [e for e in expenses if datetime.strptime(e[5], '%Y-%m-%d') >= start_of_week]
    total = sum(e[1] for e in weekly_expenses)
    by_category = {}
    for e in weekly_expenses:
        key = f"{e[2]} - {e[3]}"
        by_category[key] = by_category.get(key, 0) + e[1]
    
    return {"total": total, "by_category": by_category}

def get_spending_trends(expenses):
    today = datetime.now()
    trends = {}
    for i in range(4):
        week_start = today - timedelta(days=today.weekday() + 7 * i)
        week_end = week_start + timedelta(days=6)
        week_expenses = [e for e in expenses if week_start <= datetime.strptime(e[5], '%Y-%m-%d') <= week_end]
        trends[f"Week {4-i}"] = sum(e[1] for e in week_expenses)
    return trends

def get_savings_streak(expenses, budget):
    if not budget:
        return 0
    today = datetime.now()
    streak = 0
    for i in range(4):
        week_start = today - timedelta(days=today.weekday() + 7 * i)
        week_end = week_start + timedelta(days=6)
        week_expenses = [e for e in expenses if week_start <= datetime.strptime(e[5], '%Y-%m-%d') <= week_end]
        week_total = sum(e[1] for e in week_expenses)
        if week_total <= budget:
            streak += 1
        else:
            break
    return streak

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'amount' in request.form:
            amount = float(request.form['amount'])
            category = request.form['category']
            subcategory = request.form['subcategory']
            description = request.form['description']
            date = request.form['date']
            add_expense(amount, category, subcategory, description, date)
        elif 'budget' in request.form:
            budget = float(request.form['budget'])
            set_budget(budget)
    
    expenses = get_expenses()
    budget = get_budget()
    notifications = analyze_spending(expenses, budget)
    weekly_summary = get_weekly_summary(expenses)
    spending_trends = get_spending_trends(expenses)
    savings_streak = get_savings_streak(expenses, budget)
    
    return render_template('index2.html', expenses=expenses, notifications=notifications, 
                          weekly_summary=weekly_summary, budget=budget, 
                          spending_trends=spending_trends, savings_streak=savings_streak)

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete(expense_id):
    delete_expense(expense_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)