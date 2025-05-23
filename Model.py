from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, VARCHAR, ForeignKey, func
from sqlalchemy.orm import relationship

# initialize database
db = SQLAlchemy()

# Database Tables
class PaperReviewers(db.Model):
    __tablename__ = 'PAPER_REVIEWERS'
    PaperID = Column('PaperID', Integer, ForeignKey('PAPERS.PaperID'), primary_key=True)
    ReviewerID = Column('ReviewerID', Integer, ForeignKey('REVIEWERS.ReviewerID'), primary_key=True)

class Authors(db.Model):
    __tablename__ = 'AUTHORS'
    AuthorID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(125), nullable=False)
    LastName = Column(String(125), nullable=False)
    papers = relationship("Papers", back_populates="author")

class Papers(db.Model):
    __tablename__ = 'PAPERS'
    PaperID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(VARCHAR(200), unique=True, nullable=False)
    AuthorID = Column(Integer, ForeignKey('AUTHORS.AuthorID'), nullable=False)
    author = relationship("Authors", back_populates="papers")
    reviewers = relationship("Reviewers", secondary=PaperReviewers.__table__, back_populates="papers")

class Reviewers(db.Model):
    __tablename__ = 'REVIEWERS'
    ReviewerID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(VARCHAR(125), nullable=False)
    LastName = Column(VARCHAR(125), nullable=False)
    ReviewerEmail = Column(VARCHAR(125), nullable=True)
    papers = relationship("Papers", secondary=PaperReviewers.__table__, back_populates="reviewers")

class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)


#any database action that need to happen on start should be placed here
def model(app):
    try:
        db.create_all()
    except Exception:
        print('Error in Model, Database tables not created.')

#query all data related to the dashboard
def dashboard_analytics():
    try:
        ReviewerCount = db.session.query(Reviewers.ReviewerID).count()
        PaperCount = db.session.query(Papers.PaperID).count()
        AuthorCount = db.session.query(Authors.AuthorID).count()
        PaperWithoutReviewer = db.session.query(func.count(Papers.PaperID)).outerjoin(PaperReviewers, Papers.PaperID == PaperReviewers.PaperID).filter(PaperReviewers.PaperID == None).scalar()
        ReviewerWithoutPaper = db.session.query(func.count(Reviewers.ReviewerID)).outerjoin(PaperReviewers, Reviewers.ReviewerID == PaperReviewers.ReviewerID).filter(PaperReviewers.ReviewerID == None).scalar()
    except Exception:
        print('dashboard_analytics() Query Failed')

    return {
        'ReviewerCount': ReviewerCount,
        'PaperCount': PaperCount,
        'AuthorCount': AuthorCount,
        'PaperWithoutReviewer': PaperWithoutReviewer,
        'ReviewerWithoutPaper': ReviewerWithoutPaper

    }

"""
Cycle through all papers starting at paper 1
if paper shows up in reviewerpaper table  less then 3 times add a paper with that id
when paper is added cycle through all reviewers
reviewers must be checked by amount of times they show up  in reviewerpaper table ordered by reviewerid
if the reviewer is not already assigned the same paperid
add the reviewer that show up the least
do this for all papers until all papers show up 3 times in the reviewerpaper table
"""
def assign_reviewers():
    try:
        papers = db.session.query(Papers).order_by(Papers.PaperID.asc()).all()
        for paper in papers:
            while db.session.query(func.count(PaperReviewers.PaperID)).filter(PaperReviewers.PaperID == paper.PaperID).scalar() < 3:
                assigned_reviewer_ids = [pr.ReviewerID for pr in db.session.query(PaperReviewers).filter(PaperReviewers.PaperID == paper.PaperID).all()]

                reviewer = db.session.query(Reviewers). \
                    outerjoin(PaperReviewers, Reviewers.ReviewerID == PaperReviewers.ReviewerID). \
                    filter(Reviewers.ReviewerID.notin_(assigned_reviewer_ids)). \
                    group_by(Reviewers.ReviewerID). \
                    order_by(func.count(PaperReviewers.PaperID).asc(), Reviewers.ReviewerID.asc()). \
                    first()

                if reviewer:
                    db.session.add(PaperReviewers(PaperID=paper.PaperID, ReviewerID=reviewer.ReviewerID))
                    db.session.commit()
                else:
                    print(f"Warning: Could not find enough reviewers for Paper ID {paper.PaperID}.")
                    break
    except Exception:
        print('assign_reviewers() function error')

