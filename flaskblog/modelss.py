from flaskblog import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint

#user_exam_association = db.Table(
#    'user_exam_association',
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('exam_id', db.Integer, db.ForeignKey('exam.id'))
#)

user_exam =  db.Table('user_exam',
    db.Column('user_id' ,db.Integer, db.ForeignKey('User.id')),
    db.Column('exam_id' ,db.Integer, db.ForeignKey('exam.id'))
)


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    course = db.Column(db.String(60), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    articles = db.relationship('Article', backref = 'author', lazy=True)#backref is like adding column to post that is named author---- lazy 14:30
    exams = db.relationship(
        'Exam',
        secondary=user_exam,
        backref='users',
        #lazy='dynamic',
        #primaryjoin="User_exam_association.c.user_id == User.id",
    )

    def __repr__(self):#how our object printed when we print them
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

'''
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):#how our object printed when we print them
        return f"Post('{self.title}', '{self.date_posted}')"
'''
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=True)



    



    
#user1 = User(username = 'Bdv', email ='Basd@gmail.com', password='pass123')