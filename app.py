from flask import Flask, render_template, redirect, url_for, session, request, jsonify
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Sample users data
users = {
    "user1": {"password": "password1", "role": "role1"},
    "user2": {"password": "password2", "role": "role2"}
}

# Mock API response
def get_role_screens():
    return {
        "role1": ['components', 'inventory', 'dashboard'],
        "role2": ['boms', 'purchaseorders', 'vendors','inventory']
    }

# Decorator to check login status
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to check user role
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('role') != role:
                return "Access Denied", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('index'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/components')
@login_required
@role_required('role1')
def components():
    return render_template('components.html')

@app.route('/inventory')
@login_required
@role_required('role1')
def inventory():
    return render_template('inventory.html')

@app.route('/dashboard')
@login_required
@role_required('role1')
def dashboard():
    return render_template('dashboard.html')

@app.route('/vendors')
@login_required
@role_required('role2')
def vendors():
    return render_template('vendors.html')

@app.route('/boms')
@login_required
@role_required('role2')
def boms():
    return render_template('boms.html')

@app.route('/purchaseorders')
@login_required
@role_required('role2')
def purchaseorders():
    return render_template('purchaseorders.html')

@app.context_processor
def inject_screens():
    role_screens = get_role_screens()
    user_role = session.get('role')
    screens = role_screens.get(user_role, [])
    return dict(screens=screens)

if __name__ == '__main__':
    app.run(debug=True)
