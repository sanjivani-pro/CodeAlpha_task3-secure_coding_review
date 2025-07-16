from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = "123456"  # ❌ Hardcoded secret key (security risk)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ("admin", "admin123"))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ❌ Vulnerable to SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(query)
        result = c.fetchone()
        conn.close()

        if result:
            return f"Welcome, {username}!"
        else:
            return "Login failed!"

    return render_template('login.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
