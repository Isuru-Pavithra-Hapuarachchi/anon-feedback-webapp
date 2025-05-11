from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import re


app = Flask(__name__)
app.secret_key = '19990621'  # Replace with something strong

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            link_id TEXT UNIQUE NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_link TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Function to check if user limit is reached
def is_user_limit_reached():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    user_count = c.fetchone()[0]
    conn.close()
    return user_count >= 25


@app.route('/')
def index():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Check if user limit is reached
    if is_user_limit_reached():
        return render_template('signup.html', error="Users are fully in the system now. Please try again later.")
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        
        # Check again if user limit is reached (in case it changed while form was open)
        if is_user_limit_reached():
            return render_template('signup.html', error="Users are fully in the system now. Please try again later.")
        
        # Validate username length (4-10 characters)
        if len(username) < 4 or len(username) > 10:
            return render_template('signup.html', error="Username must be 4-10 characters long.")
            
        # Validate password length (4-10 characters)
        if len(password) < 4 or len(password) > 10:
            return render_template('signup.html', error="Password must be 4-10 characters long.")
        
        if password != confirm:
            return render_template('signup.html', error="Passwords do not match")
        
        link_id = str(uuid.uuid4())[:8]
        hashed_password = generate_password_hash(password)
        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, link_id) VALUES (?, ?, ?)",
                      (username, hashed_password, link_id))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('signup.html', error="Username already exists")
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT password, link_id FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        if result and check_password_hash(result[0], password):
            session['username'] = username
            session['link_id'] = result[1]
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

# Dashboard (only for logged in users)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    link_id = session['link_id']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT content FROM messages WHERE recipient_link = ?", (link_id,))
    messages = c.fetchall()
    conn.close()
    
   # Handle AJAX requests for auto-refresh
    if request.args.get('ajax') == 'true':
        message_contents = [msg[0] for msg in messages]
        return jsonify({
            'messages': message_contents,
            'count': len(messages)
        })
    
    # Regular page load
    return render_template('dashboard.html', messages=messages, link_id=link_id)


@app.route('/m/<link_id>', methods=['GET', 'POST'])
def message_form(link_id):
    if request.method == 'POST':
        content = request.form['content']
        word_count = len(content.strip().split())

        if word_count > 150:
            return render_template('message_form.html', error="Message exceeds 150-word limit.", content=content)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (recipient_link, content) VALUES (?, ?)", (link_id, content))
        conn.commit()
        conn.close()
        return redirect(url_for('prompt'))

    return render_template('message_form.html')

@app.route('/prompt')
def prompt():
    return render_template('prompt.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
