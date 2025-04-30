# main.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from Model import db, User, create_tables  # ✅ Import models and db instance properly

DATABASE_USER = 'abc'
DATABASE_PASSWD = 'abc123'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWD}@localhost/AdminDashboard'
app.config['SECRET_KEY'] = 'your_secret_key'

bcrypt = Bcrypt(app)
db.init_app(app)  # ✅ Proper initialization of SQLAlchemy

@app.route('/')
def Dashboard():
    return render_template('Dashboard.html')

@app.route('/reviewers')
def Reviewer():
    return render_template('Reviewer.html')

@app.route('/authors')
def Author():
    return render_template('Author.html')

@app.route('/papers')
def Paper():
    return render_template('Papers.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('Paper'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    return render_template('AdminDashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_tables(app)  # ✅ Tables created within app context
    app.run(debug=True, host='127.0.0.1', port=5000)
