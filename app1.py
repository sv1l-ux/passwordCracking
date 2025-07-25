# app1.py
# ============================================================================
# VULNERABILITY DEMONSTRATION: Unsalted SHA1 + SQL Injection
# ============================================================================
# WARNING: This code is intentionally vulnerable for educational purposes.
# DO NOT USE IN PRODUCTION.
#
# SECURITY ISSUES DEMONSTRATED:
# 1. SQL Injection - Direct string concatenation in queries
# 2. Unsalted SHA1 hashing - Fast and vulnerable to rainbow table attacks
# 3. No input validation or sanitization
# 4. Database error leakage - Raw errors returned to user
#
# PURPOSE: Demonstrate the most basic vulnerabilities that SQLMap can exploit
# NEXT STEP: See app2.py for salted SHA1 improvements
#
# This is FULLY vulnerable application.
# Suggestions to fix are as follows:
#   * use a salt which is a random value added to the password before hashing
#     and then store the salt with the hash in the database
#   * use a stronger hashing algorithm like bcrypt or Argon2
# ============================================================================

from flask import Flask, request, render_template_string, g
import sqlite3
import hashlib
import os

app = Flask(__name__)
DATABASE = 'users1.db'

# Common test passwords (included in wordlist.txt)
TEST_USERS = [
    ('admin', 'password123'),
    ('user1', 'admin'),
    ('user2', '123456'),
    ('john', 'qwerty'),
    ('jane', 'letmein')
]

def get_db():
    """Opens a new database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Closes the database connection."""
    if hasattr(g, 'db'):
        g.db.close()

def init_db():
    """Initialize database with vulnerable SHA1 hashes (no salt).
    FOR DEMO PURPOSES TO MAKE IT EASY
    """
    with app.app_context():
        db = get_db()
        
        # Create simple users table
        db.cursor().executescript("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)
        
        # Insert test users with SHA1 hashes (VULNERABILITY: No salt!)
        cursor = db.cursor()
        for username, password in TEST_USERS:
            # VULNERABILITY: SHA1 with no salt = rainbow table attack
            # Hex Digest of password becomes a string
            password_hash = hashlib.sha1(password.encode()).hexdigest()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                         (username, password_hash))
        
        db.commit()
        print(f"Created {len(TEST_USERS)} test users with SHA1 hashes")

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    VULNERABILITY DEMO: SQL Injection + Unsalted SHA1
    
    This function demonstrates the most basic web application vulnerabilities:
    1. SQL injection via string concatenation
    2. Weak password hashing (SHA1, no salt)
    3. Error information leakage
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor()
        
        # VULNERABILITY: Direct string concatenation allows SQL injection
        # SQLMap will easily exploit this to extract the entire database
        query = f"SELECT * FROM users WHERE username = '{username}'"
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()

            if user:
                # VULNERABILITY: SHA1 with no salt (fast to crack)
                password_hash = hashlib.sha1(password.encode()).hexdigest()
                if user[2] == password_hash:
                    return f"<h2>Login Successful!</h2><p>Welcome {user[1]}</p>"
                else:
                    return "<h2>Invalid Credentials</h2>"
            else:
                return "<h2>Invalid Credentials</h2>"
                
        except sqlite3.Error as e:
            # VULNERABILITY: Raw database errors leaked to user
            # This makes SQLMap detection trivial
            return f"<h1>Database Error</h1><pre>Error: {e}</pre>"

    # Simplified HTML template for demo
    return render_template_string('''
        <!doctype html>
        <html>
            <head>
                <title>App 1: Unsalted SHA1 (Most Vulnerable)</title>

            </head>
            <body>
                <div class="container">
                    <h1>App 1: Most Vulnerable</h1>
                    
                    <div class="warning">
                        WARNING: INTENTIONALLY VULNERABLE - Educational Use Only
                    </div>
                    
                    <div class="vuln-list">
                        <h3>Vulnerabilities:</h3>
                        <ul>
                            <li><strong>SQL Injection</strong> - String concatenation</li>
                            <li><strong>Unsalted SHA1</strong> - Fast rainbow table attacks</li>
                            <li><strong>Error Leakage</strong> - Raw database errors exposed</li>
                            <li><strong>No Input Validation</strong> - Direct processing</li>
                        </ul>
                    </div>
                    
                    <form method="post">
                        <h3>Login Test:</h3>
                        <input type="text" name="username" placeholder="Username (try: admin)" required>
                        <input type="password" name="password" placeholder="Password (try: password123)" required>
                        <button type="submit" class="btn">Login</button>
                    </form>
                    
                    <div class="test-creds">
                        <h3>Test Credentials:</h3>
                        <ul>
                            <li>admin / password123</li>
                            <li>user1 / admin</li>
                            <li>user2 / 123456</li>
                        </ul>
                    </div>
                    
                    <h3>SQLMap Test:</h3>
                    <code>sqlmap -u "http://localhost:5001" --data="username=admin&password=test" --dump</code>
                    
                    <hr>
                    <p><strong>Next:</strong> See <a href="http://localhost:5002">App 2</a> for salted SHA1 improvements</p>
                </div>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    print("=" * 60)
    print("STARTING APP 1: Most Vulnerable (Unsalted SHA1)")
    print("=" * 60)
    print("Port: 5001")
    print("Database: users1.db")
    print("Hash Algorithm: SHA1 (no salt)")
    print("WARNING: This application is intentionally vulnerable!")
    print("=" * 60)
    
    # Clean start
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    
    init_db()
    app.run(debug=True, port=5001, host='0.0.0.0') 