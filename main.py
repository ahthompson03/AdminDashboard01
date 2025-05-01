from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import Model as Model

DATABASE_USER = 'abc'
DATABASE_PASSWD = 'abc123'

#initialize App and DataBase
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://abc:abc123@localhost/users_db'
#DataBase Config
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWD}@localhost/AdminDashboard'
app.config['SECRET_KEY'] = 'your_secret_key'

bcrypt = Bcrypt(app)
Model.db.init_app(app)

#username = 'test@jack.com'

# ROUTES

@app.route('/dash')
def Dashboard():
    queryResults = Model.DashBoardAnalytics()
    return render_template('Dashboard.html',
                           ReviewerCount = queryResults['ReviewerCount'],
                           PaperCount = queryResults['PaperCount'],
                           AuthorCount = queryResults['AuthorCount'],
                           PaperWithoutReviewer = queryResults['PaperWithoutReviewer'],
                           ReviewerWithoutPaper = queryResults['ReviewerWithoutPaper'])

@app.route('/papers')
def Paper():
    queryResults = Model.PaperQuerys()
    return render_template('Papers.html',
                          )
    # Title = json.dumps(queryResults[0])
                           #Author = queryResults[1],
                          # PaperID = queryResults[2])


@app.route('/reviewers')
def Reviewer():
    return render_template('Reviewer.html')


@app.route('/authors')
def Author():
    authors = Model.Authors.query.all()
    return render_template('Author.html', authors=authors)





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = Model.User(username=username, password=hashed_password)
        Model.db.session.add(user)
        Model.db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Model.User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('Dashboard'))
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


@app.route('/add_author', methods=['POST'])
def add_author():
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    new_author = Model.Authors(FirstName=first_name, LastName=last_name)
    Model.db.session.add(new_author)
    Model.db.session.commit()

    flash('Author added successfully!', 'success')
    return redirect(url_for('Author'))


if __name__ == '__main__':
    with app.app_context():
        Model.Model(app)
    app.run(debug=True, host='127.0.0.1', port=5000)
