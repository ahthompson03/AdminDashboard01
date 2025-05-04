from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import Model as Model

#database global variables
DATABASE_USER = 'abc'
DATABASE_PASSWD = 'abc123'

#initialize App
app = Flask(__name__)

#DataBase and app Config
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWD}@localhost/AdminDashboard'
app.config['SECRET_KEY'] = 'your_secret_key'

#initialize bcrypt
bcrypt = Bcrypt(app)
#create reference to database and initialize
Model.db.init_app(app)

#username = 'test@jack.com'

# ROUTES
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
            return redirect(url_for('dashboard_viewer_controller'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))




"""Dashboard: Viewer/Controller Consists of only one page named dashboard_viewer_controller"""
@app.route('/dashboard')
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
def paper_viewer_controller():
    papers = Model.db.session.query(Model.Authors, Model.Papers).join(Model.Papers, Model.Authors.AuthorID == Model.Papers.AuthorID).order_by(Model.Papers.PaperID).all()
    return render_template('Papers.html', papers = papers)


@app.route('/add_paper', methods=['POST'])
def add_paper():
    title = request.form['title']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
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
        flash('Paper added successfully!', 'success')
        return redirect(url_for('paper_viewer_controller'))
    else:
        flash('Paper Already Exists!', 'warning')
        return redirect(url_for('paper_viewer_controller'))


@app.route('/delete_paper', methods=['POST'])
def delete_paper():
    paper_id = request.form['paper_id']
    paper = Model.Papers.query.get(paper_id)
    if not paper:
        flash(f"No Paper found with ID: {paper_id}.", "warning")
        return redirect(url_for('paper_viewer_controller'))
    Model.db.session.delete(paper)
    Model.db.session.commit()
    return redirect(url_for('paper_viewer_controller'))


@app.route('/auto_assign', methods=['POST'])
def auto_assign():
    Model.Assign_Reviewers()
    return redirect(url_for('paper_viewer_controller'))



"""Reviewer: Viewer/Controller Consists of main page 'reviewer_viewer_controller', subpage 'add_reviewer', and subpage 'delete_reviewer'"""
@app.route('/reviewers')
def reviewer_viewer_controller():
    reviewers = Model.Reviewers.query.all()
    return render_template('Reviewer.html', reviewers=reviewers)


@app.route('/add_reviewer', methods=['POST'])
def add_reviewer():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    new_reviewer = Model.Reviewers(FirstName=first_name, LastName=last_name)
    Model.db.session.add(new_reviewer)
    Model.db.session.commit()
    flash('Reviewer added successfully!', 'success')
    return redirect(url_for('reviewer_viewer_controller'))


@app.route('/delete_reviewer', methods=['POST'])
def delete_reviewer():
    reviewer_id = request.form['reviewer_id']
    reviewer = Model.Reviewers.query.get(reviewer_id)
    if not reviewer:
        flash(f"No Reviewer found with ID: {reviewer_id}.", "warning")
        return redirect(url_for('reviewer_viewer_controller'))
    #Remove paper associations first
    Model.Papers.query.filter_by(ReviewerID=reviewer_id).update({Model.Papers.ReviewerID: None})
    #Then delete the reviewer
    Model.db.session.delete(reviewer)
    Model.db.session.commit()
    return redirect('reviewers')


"""Author: Viewer/Controller Consists of main page 'author_viewer_controller', subpage 'add_author', and subpage 'delete_author'"""
@app.route('/authors')
def author_viewer_controller():
    authors = Model.Authors.query.all()
    return render_template('Author.html', authors=authors)


@app.route('/add_author', methods=['POST'])
def add_author():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    new_author = Model.Authors(FirstName=first_name, LastName=last_name)
    Model.db.session.add(new_author)
    Model.db.session.commit()
    flash('Author added successfully!', 'success')
    return redirect(url_for('author_viewer_controller'))


@app.route('/delete_author', methods=['POST'])
def delete_author():
    author_id = request.form['author_id']
    author = Model.Authors.query.get(author_id)
    if not author:
        flash(f"No author found with ID: {author_id}.", "warning")
        return redirect(url_for('author_viewer_controller'))
    # First delete all papers linked to this author
    Model.Papers.query.filter_by(AuthorID=author_id).delete()
    # Then delete the author
    Model.db.session.delete(author)
    Model.db.session.commit()
    return redirect('/authors')



if __name__ == '__main__':
    with app.app_context():
        Model.Model(app)
    app.run(debug=True, host='127.0.0.1', port=5000)


