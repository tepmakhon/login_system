from flask import Flask, render_template, request, redirect, session, flash
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# File to store user data
USER_FILE = 'users.txt'

# Helper: Save user credentials to the file
def save_user(username, hashed_password):
    with open(USER_FILE, 'a') as file:
        file.write(f"{username},{hashed_password.decode('utf-8')}\n")

# Helper: Check if a user exists and validate password
def validate_user(username, password):
    try:
        with open(USER_FILE, 'r') as file:
            users = file.readlines()
        for user in users:
            stored_username, stored_password = user.strip().split(',')
            if stored_username == username and bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True
    except FileNotFoundError:
        pass  # File doesn't exist yet
    return False

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect('/login')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save the user credentials
        save_user(username, hashed_password)
        flash('Signup successful! Please log in.')
        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate credentials
        if validate_user(username, password):
            session['username'] = username
            return redirect('/')
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)