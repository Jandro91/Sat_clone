from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import csv

app = Flask(__name__)

def load_users():
    users = {}
    with open('users.csv', newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            users[row['login']] = {'password': row['password'], 'pdf_file': row['pdf_file']}
    return users

USERS = load_users()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form['login']
        p = request.form['password']
        user = USERS.get(u)
        if user and user['password'] == p:
            return redirect(url_for('certificate', filename=user['pdf_file']))
        error = 'Incorrect username or password'
    return render_template('login.html', error=error)

@app.route('/certificate/<filename>')
def certificate(filename):
    return render_template('certificate.html', filename=filename)

@app.route('/certificates/<filename>')
def download_file(filename):
    return send_from_directory('certificates', filename)

if __name__ == '__main__':
    print("Starting College Board clone...")
    app.run(host='0.0.0.0', port=80, debug=True)
