from flask import Flask, render_template, request, redirect, url_for, jsonify
from tracker import insert_expense, insert_household_members, insert_income
import sqlite3
import datetime
##hey

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def index():
   return render_template("index.html")



@app.route('/add/income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        date = request.form.get('date')
        member_name = request.form.get('memberName')
        income_category = request.form.get('Income_category')
        description = request.form.get('Income_description')
        amount = request.form.get('Income_amount')

        insert_income(date, member_name, income_category, description, amount)
        return redirect(url_for('index'))
    else:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Income")
            income_data = cur.fetchall()
            cur.execute("SELECT MemberName FROM HouseholdMember")
            members = [row[0] for row in cur.fetchall()]
        if income_data:
            return render_template('add/income.html', data=income_data, members=members)
        else:
            return render_template('add/income.html', data=None, members=members)
        

@app.route('/add/expense', methods=['GET', 'POST'])
def expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['Expense_category']
        description = request.form['Expense_description']
        amount = request.form['Expense_amount']
        member_name = request.form['memberName']
        insert_expense(date, category, description, amount, member_name)
        return redirect(url_for('index'))
    else:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT MemberName FROM HouseholdMember")
            members = [row[0] for row in cur.fetchall()]
        return render_template('add/expense.html', members=members)
    

@app.route('/view/overview', methods=['GET'])
def overview():
    month = request.args.get('month', default=str(datetime.datetime.now().month))
    year = request.args.get('year', default=str(datetime.datetime.now().year))
    month = month.zfill(2)

    with sqlite3.connect('database.db') as conn:
        conn.row_factory = dict_factory  
        cur = conn.cursor()
        cur.execute("""
            SELECT Date, MemberName, ExpenseCategory as Category, Description, -Amount as Amount
            FROM Expense
            WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
            UNION ALL
            SELECT Date, MemberName, IncomeCategory as Category, Description, Amount
            FROM Income
            WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
            ORDER BY Date
        """, (month, year, month, year))
        records = cur.fetchall()

        cur.execute("""
            SELECT 'Income' as Type, IncomeCategory as Category, SUM(Amount) as Total
            FROM Income
            WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
            GROUP BY IncomeCategory
            UNION ALL
            SELECT 'Expense' as Type, ExpenseCategory, -SUM(Amount) as Total
            FROM Expense
            WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
            GROUP BY ExpenseCategory
        """, (month, year, month, year))
        summary = cur.fetchall()

    return render_template('view/overview.html', records=records, summary=summary, month=month, year=year)


if __name__ == "__main__":
   app.run(debug=True)


##Hello 

#hey
##hey 
