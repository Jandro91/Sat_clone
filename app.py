from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import csv
import os

app = Flask(__name__)
app.secret_key = 'sat-clone-secret-123'

def load_users():
    users = {}
    with open('users.csv', newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            users[row['login']] = row
    return users

USERS = load_users()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form['login']
        p = request.form['password']
        user = USERS.get(u)
        if user and user['password'] == p:
            session['username'] = u
            return redirect(url_for('certificate', filename=user['pdf_file'], username=u))
        error = 'Incorrect username or password'
    return render_template('login.html', error=error)

@app.route('/certificate/<filename>')
def certificate(filename):
    username = session.get('username', 'Unknown')
    return render_template('certificate.html', filename=filename, username=username)

@app.route('/certificates/<filename>')
def download_file(filename):
    return send_from_directory('certificates', filename)

# ✅ Только один правильный запуск приложения
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Для Render
    app.run(host="0.0.0.0", port=port)
