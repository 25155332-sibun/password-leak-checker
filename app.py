import hashlib
import requests
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize DB if it doesn't exist
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_value TEXT,
            result TEXT,
            strength TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# k-Anonymity password check (100% Free & Secure)
def check_password_pwned(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Error fetching data from API", 0
    
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return True, int(count)
            
    return False, 0

# Enhanced password strength analyzer
def analyze_strength(password):
    score = 0
    
    # Length checks
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 1
    
    # Complexity checks
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1
    
    # Score mapping (Max score is 7)
    if score <= 3: 
        return "Weak"
    elif score <= 5: 
        return "Medium"
    else: 
        return "Strong"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    strength = None
    if request.method == 'POST':
        password = request.form.get('query_value')
        
        is_pwned, count = check_password_pwned(password)
        strength = analyze_strength(password)
        
        if is_pwned:
            result = f"⚠️ Unsafe! This password has been exposed in {count:,} data breaches."
        else:
            result = "✅ Safe! This password was not found in any known public data leaks."
        
        # Save to SQLite history (Masking the actual password for privacy)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (query_value, result, strength) VALUES (?, ?, ?)",
                       ('••••••••', result, strength))
        conn.commit()
        conn.close()

    return render_template('index.html', result=result, strength=strength)

@app.route('/history')
def history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT query_value, result, strength, timestamp FROM history ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    return render_template('report.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)