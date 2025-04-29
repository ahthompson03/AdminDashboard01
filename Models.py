from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

DATABASE_USER = 'abc'
DATABASE_PASSWD = 'abc123'

app = Flask(__name__)
#DataBase Config
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWD}@localhost/AdminDashboard'
app.config['SECRET_KEY'] = 'your_secret_key'
#initialize database
db = SQLAlchemy(app)


#Database Tables
class Authors(db.Model):
    __tablename__ = 'AUTHORS'

    AuthorID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(VARCHAR(25), nullable=False)
    LastName = Column(VARCHAR(25), nullable=False)
    papers = relationship("Paper", back_populates="author")

class Papers(db.Model):
    __tablename__ = 'PAPERS'

    PaperID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(VARCHAR(200), unique = True, nullable=False)
    AuthorID = Column(Integer, ForeignKey('AUTHORS.AuthorID'), nullable=False)
    ReviewerID = Column(Integer, ForeignKey('REVIEWERS.ReviewerID'), nullable=True)
    author = relationship("Author", back_populates="papers")
    reviewer = relationship("Reviewer", back_populates="papers")
    track = relationship("Track", back_populates="paper")

class Reviewer(db.Model):
    __tablename__ = 'REVIEWERS'

    ReviewerID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(VARCHAR(25), nullable=False)
    LastName = Column(VARCHAR(25), nullable=False)

class Track(db.Model):
    __tablename__ = 'TRACKS'

    TrackID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False)
    PaperID = Column(Integer, ForeignKey('PAPERS.PaperID'), nullable=True)
    paper = relationship("Paper", back_populates="track")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()