
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship


#initialize database
db = SQLAlchemy()

#Database Tables
class Authors(db.Model):
    __tablename__ = 'AUTHORS'
    AuthorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(25), nullable=False)
    LastName = db.Column(db.String(25), nullable=False)
    papers = db.relationship("Papers", back_populates="author")


class Papers(db.Model):
    __tablename__ = 'PAPERS'

    PaperID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(VARCHAR(200), unique=True, nullable=False)
    AuthorID = Column(Integer, ForeignKey('AUTHORS.AuthorID'), nullable=False)
    ReviewerID = Column(Integer, ForeignKey('REVIEWERS.ReviewerID'), nullable=True)

    author = relationship("Authors", back_populates="papers")
    reviewer = relationship("Reviewer", back_populates="papers")
    track = relationship("Track", back_populates="paper")

class Reviewer(db.Model):
    __tablename__ = 'REVIEWERS'
    ReviewerID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(VARCHAR(25), nullable=False)
    LastName = Column(VARCHAR(25), nullable=False)
    papers = relationship("Papers", back_populates="reviewer")

class Track(db.Model):
    __tablename__ = 'TRACKS'
    TrackID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False)
    PaperID = Column(Integer, ForeignKey('PAPERS.PaperID'), nullable=True)
    paper = relationship("Papers", back_populates="track")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

def Model(app):
        db.create_all()



def DashBoardAnalytics():

    ReviewerCount = db.session.query(Reviewer.ReviewerID).count()
    PaperCount = db.session.query(Papers.PaperID).count()
    AuthorCount = db.session.query(Authors.AuthorID).count()
    PaperWithoutReviewer = db.session.query(Papers).filter(Papers.ReviewerID.is_(None)).count()
    ReviewerWithoutPaper = db.session.query(db.func.count(Reviewer.ReviewerID)). \
        outerjoin(Papers, Reviewer.ReviewerID == Papers.ReviewerID). \
        filter(Papers.PaperID == None). \
        scalar()

    return {
    'ReviewerCount': ReviewerCount,
    'PaperCount': PaperCount,
    'AuthorCount': AuthorCount,
    'PaperWithoutReviewer': PaperWithoutReviewer,
    'ReviewerWithoutPaper': ReviewerWithoutPaper

    }

def PaperQuerys():
    papers = db.session.query(Papers).all()
    title = []
    authorName = db.session.query(Authors.FirstName).join(Papers, Authors.AuthorID == Papers.AuthorID).order_by(Papers.Title).all()
    paperID = []

    for item in papers:
        title.append(item.Title)
        paperID.append(item.PaperID)

    #tuple is used to protect the data since it will no longer need changed.
    return (
        title,
        authorName,
        paperID
    )

