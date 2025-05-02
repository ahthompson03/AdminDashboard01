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
    ReviewerID1 = Column(Integer, ForeignKey('REVIEWERS.ReviewerID'), nullable=True)
    ReviewerID2 = Column(Integer, ForeignKey('REVIEWERS.ReviewerID'), nullable=True)
    ReviewerID3 = Column(Integer, ForeignKey('REVIEWERS.ReviewerID'), nullable=True)


    author = relationship("Authors", back_populates="papers")
    reviewer = relationship("Reviewers", back_populates="papers")  # update to match new class name
    track = relationship("Track", back_populates="paper")

class Reviewers(db.Model):  # renamed from Reviewer
    __tablename__ = 'REVIEWERS'
    ReviewerID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(VARCHAR(25), nullable=False)
    LastName = Column(VARCHAR(25), nullable=False)
    ReviewerEmail = Column(VARCHAR(25), nullable=True)
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

    ReviewerCount = db.session.query(Reviewers.ReviewerID).count()
    PaperCount = db.session.query(Papers.PaperID).count()
    AuthorCount = db.session.query(Authors.AuthorID).count()
    PaperWithoutReviewer = db.session.query(Papers).filter(Papers.ReviewerID.is_(None)).count()
    ReviewerWithoutPaper = db.session.query(db.func.count(Reviewers.ReviewerID)). \
        outerjoin(Papers, Reviewers.ReviewerID == Papers.ReviewerID). \
        filter(Papers.PaperID == None). \
        scalar()

    return {
    'ReviewerCount': ReviewerCount,
    'PaperCount': PaperCount,
    'AuthorCount': AuthorCount,
    'PaperWithoutReviewer': PaperWithoutReviewer,
    'ReviewerWithoutPaper': ReviewerWithoutPaper

    }
#
"""
Least amount of papers
By ID
Until every paper has 3 reviewers
Check for duplicate Reviewers

Give every reviewer 1 paper, then 2 papers, then 3 or until papers run out


Go through papers and make a list of all papers that don't have 3 reviewers
Second list (ReviewerIDList) of all reviewer ID's that show up in the papers
Dictionary with key of ReviewerID and Value of amount of times it shows up in Reviewer list
Find lowest integer in the list and assign it to the paper with the lowest amount of reviewers 



"""