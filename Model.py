
import main as viewer
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship



#initialize database
db = SQLAlchemy(viewer.app)


#Database Tables
class Authors(db.Model):
    __tablename__ = 'AUTHORS'

    AuthorID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(VARCHAR(25), nullable=False)
    LastName = Column(VARCHAR(25), nullable=False)
    papers = relationship("Papers", back_populates="author")

class Papers(db.Model):
    __tablename__ = 'PAPERS'

    PaperID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(VARCHAR(200), unique = True, nullable=False)
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

def CreateTables():
    with viewer.app.app_context():
        db.create_all()