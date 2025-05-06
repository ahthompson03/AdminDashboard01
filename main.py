from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from flask_bcrypt import Bcrypt
import Model as Model
from functools import wraps

#database global variables
DATABASE_USER = 'abc'
DATABASE_PASSWD = 'abc123'

#initialize App
app = Flask(__name__)

#DataBase and app Config
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWD}@localhost/AdminDashboard'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

#initialize bcrypt
bcrypt = Bcrypt(app)
#create reference to database and initialize
Model.db.init_app(app)
#create reference to the current session
Session(app)


#Session tracking
def is_authenticated():
    username = session.get('username')
    return username

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# ROUTES
@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard_viewer_controller'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = Model.User(username=username, password=hashed_password)
        try:
            Model.db.session.add(user)
            Model.db.session.commit()
        except Exception:
            print('Failed to add user to database')
            return render_template('register.html')

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = Model.User.query.filter_by(username=username).first()
        except Exception:
            print('Query Failed')
            return render_template('login.html')

        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard_viewer_controller'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



"""Dashboard: Viewer/Controller Consists of only one page named dashboard_viewer_controller"""
@app.route('/dashboard')
@login_required
def dashboard_viewer_controller():
    queryResults = Model.DashBoardAnalytics()
    return render_template('Dashboard.html',
                           ReviewerCount = queryResults['ReviewerCount'],
                           PaperCount = queryResults['PaperCount'],
                           AuthorCount = queryResults['AuthorCount'],
                           PaperWithoutReviewer = queryResults['PaperWithoutReviewer'],
                           ReviewerWithoutPaper = queryResults['ReviewerWithoutPaper'])




"""Paper: Viewer/Controller Consists of main page 'paper_viewer_controller', subpage 'add_paper',subpage 'delete_paper, and subpage 'auto_assign'"""
@app.route('/papers')
@login_required
def paper_viewer_controller():
    try:
        papers = Model.db.session.query(Model.Authors, Model.Papers).join(Model.Papers, Model.Authors.AuthorID == Model.Papers.AuthorID).order_by(Model.Papers.PaperID).all()
    except Exception:
        print('Query Failed')
        return render_template('Papers.html')
    return render_template('Papers.html', papers = papers)


@app.route('/add_paper', methods=['POST'])
@login_required
def add_paper():
    title = request.form['title']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    try:
        author = Model.Authors.query.filter_by(FirstName=first_name, LastName=last_name).first()
        if not author:
            author = Model.Authors(FirstName=first_name, LastName=last_name)
            Model.db.session.add(author)
            Model.db.session.commit()
        else:
            author_id = author.AuthorID
        new_paper = Model.Papers.query.filter_by(Title=title).first()
        #check to see if paper exists if not it will create one
        if not new_paper:
            new_paper = Model.Papers(Title=title, AuthorID=author.AuthorID)
            Model.db.session.add(new_paper)
            Model.db.session.commit()
            print(Model.Papers.query.filter_by(Title=title).first())
            return redirect(url_for('paper_viewer_controller'))
        else:
            return redirect(url_for('paper_viewer_controller'))
    except Exception:
        print('Error in adding paper')
        return redirect(url_for('paper_viewer_controller'))


@app.route('/delete_paper', methods=['POST'])
@login_required
def delete_paper():
    paper_id = request.form['paper_id']
    try:
        paper_reviewers = Model.db.session.query(Model.PaperReviewers).join(Model.Papers, Model.PaperReviewers.PaperID == Model.Papers.PaperID).filter(Model.Papers.PaperID == paper_id).all()
        paper = Model.db.session.query(Model.Papers).filter(Model.Papers.PaperID == paper_id).first()
        if not paper:
            print('paper not found')
            return redirect(url_for('paper_viewer_controller'))
        for paperreviewer in paper_reviewers:
            Model.db.session.delete(paperreviewer)
        Model.db.session.delete(paper)
        Model.db.session.commit()
        return redirect(url_for('paper_viewer_controller'))
    except Exception:
        print('Error in deleting paper')
        return redirect(url_for('paper_viewer_controller'))


@app.route('/auto_assign', methods=['POST'])
@login_required
def auto_assign():
    Model.Assign_Reviewers()
    return redirect(url_for('paper_viewer_controller'))



"""Reviewer: Viewer/Controller Consists of main page 'reviewer_viewer_controller', subpage 'add_reviewer', and subpage 'delete_reviewer'"""
@app.route('/reviewers')
@login_required
def reviewer_viewer_controller():
    try:
        reviewers = Model.Reviewers.query.all()
    except Exception:
        print('Query Failed')
        return render_template('Reviewer.html')
    return render_template('Reviewer.html', reviewers=reviewers)


@app.route('/add_reviewer', methods=['POST'])
@login_required
def add_reviewer():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    new_reviewer = Model.Reviewers(FirstName=first_name, LastName=last_name)
    try:
        Model.db.session.add(new_reviewer)
        Model.db.session.commit()
        return redirect(url_for('reviewer_viewer_controller'))
    except Exception:
        print('Error in adding reviewer')
        return redirect(url_for('reviewer_viewer_controller'))


@app.route('/delete_reviewer', methods=['POST'])
@login_required
def delete_reviewer():
    reviewer_id = request.form['reviewer_id']
    try:
        paper_reviewers = Model.db.session.query(Model.PaperReviewers).join(Model.Papers, Model.PaperReviewers.PaperID == Model.Papers.PaperID).filter(Model.Papers.PaperID == reviewer_id).all()
        reviewer = Model.db.session.query(Model.Reviewers).filter(Model.Reviewers.ReviewerID == reviewer_id).first()
        if not reviewer:
            return redirect(url_for('reviewer_viewer_controller'))
        for paperreviewer in paper_reviewers:
            Model.db.session.delete(paperreviewer)
        #Then delete the reviewer
        Model.db.session.delete(reviewer)
        Model.db.session.commit()
        return redirect('reviewers')
    except Exception:
        print('Error in deleting reviewer')
        return redirect(url_for('reviewer_viewer_controller'))

"""Author: Viewer/Controller Consists of main page 'author_viewer_controller', subpage 'add_author', and subpage 'delete_author'"""
@app.route('/authors')
@login_required
def author_viewer_controller():
    try:
        authors = Model.Authors.query.all()
    except Exception:
        print('Query Failed')
        return render_template('Author.html')
    return render_template('Author.html', authors=authors)


@app.route('/add_author', methods=['POST'])
@login_required
def add_author():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    new_author = Model.Authors(FirstName=first_name, LastName=last_name)
    try:
        Model.db.session.add(new_author)
        Model.db.session.commit()
        return redirect(url_for('author_viewer_controller'))
    except Exception:
        print('Error in adding author')
        return redirect(url_for('author_viewer_controller'))


@app.route('/delete_author', methods=['POST'])
@login_required
def delete_author():
    author_id = request.form['author_id']
    try:
        papers = Model.db.session.query((Model.Papers)).filter(Model.Papers.AuthorID == author_id).all()
        paper_reviewers = Model.db.session.query(Model.PaperReviewers).join(Model.Papers, Model.PaperReviewers.PaperID == Model.Papers.PaperID).filter(Model.Papers.AuthorID == author_id).all()
        author = Model.db.session.query(Model.Authors).filter(Model.Authors.AuthorID == author_id).first()
        if not author:
            return redirect(url_for('author_viewer_controller'))
        for paperreviewer in paper_reviewers:
            Model.db.session.delete(paperreviewer)
        for paper in papers:
            Model.db.session.delete(paper)
        Model.db.session.delete(author)
        Model.db.session.commit()
        return redirect('/authors')
    except Exception:
        print('Error in deleting author')
        return redirect(url_for('author_viewer_controller'))



if __name__ == '__main__':
    with app.app_context():
        Model.Model(app)
    app.run(debug=True, host='127.0.0.1', port=5000)


