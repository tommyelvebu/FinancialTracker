import sqlite3

def create_tables():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()

        # Create HouseholdMember table
        c.execute('''
        CREATE TABLE IF NOT EXISTS HouseholdMember (
          MemberName TEXT PRIMARY KEY
        );
        ''')

        # Create Expense table
        c.execute('''
        CREATE TABLE IF NOT EXISTS Expense (
          ExpenseID INTEGER PRIMARY KEY AUTOINCREMENT,
          Date TEXT NOT NULL,
          ExpenseCategory TEXT NOT NULL,
          Description TEXT NOT NULL,
          Amount REAL NOT NULL,
          MemberName TEXT,
          FOREIGN KEY (MemberName) REFERENCES HouseholdMember(MemberName)
        );
        ''')

        # Create Income table
        c.execute('''
        CREATE TABLE IF NOT EXISTS Income (
          IncomeID INTEGER PRIMARY KEY AUTOINCREMENT,
          Date TEXT NOT NULL,
          IncomeCategory TEXT NOT NULL,
          Description TEXT NOT NULL,
          Amount REAL NOT NULL,
          MemberName TEXT,
          FOREIGN KEY (MemberName) REFERENCES HouseholdMember(MemberName)
        );
        ''')

        members = ["Tommy Elvebu", "Madalynn Younts"]
        c.executemany('INSERT OR IGNORE INTO HouseholdMember (MemberName) VALUES (?)', [(name,) for name in members])

        conn.commit()

if __name__ == '__main__':
    create_tables()

def insert_expense(date, category, description, amount, member_name):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO Expense (Date, ExpenseCategory, Description, Amount, MemberName) 
            VALUES (?, ?, ?, ?, ?)
        """, (date, category, description, amount, member_name))
        conn.commit()


def insert_income(date, member_name, income_category, description, amount):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO Income (Date, MemberName, IncomeCategory, Description, Amount) 
            VALUES (?, ?, ?, ?, ?)
        """, (date, member_name, income_category, description, amount))
        conn.commit()

def insert_household_members():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        names = ["Tommy Elvebu", "Madalynn Younts", "Philip Walekhwa", "Martin Dimmen", "Puskar Acharya", "Lars Monsen"]
        for name in names:
            c.execute('INSERT OR IGNORE INTO HouseholdMember (MemberName) VALUES (?)', (name,))
        conn.commit()

if __name__ == '__main__':
    create_tables()
    insert_household_members()

