from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager




app= Flask(__name__)

app.config['SECRET_KEY'] = 'erpvmefvnwkvmmwvwewvlw;rvwrkvmwrvw'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'




db = SQLAlchemy(app)


from .modelss import User

#from .modelss import user1
with app.app_context():
        db.create_all()
        
        #you cant use this now because there is user with these values in the database you must change
        
        #db.session.add(user1)
        #db.session.commit()

login_manager = LoginManager()
login_manager.login_view = 'login' # (login_view) tell us where we need to go when we are not logged in
login_manager.init_app(app) # tell the login manager what app we are using

@login_manager.user_loader
def load_user(id):  # telling flask how we load a user
        return User.query.get(int(id))  # it work like filter_by but by default it looks for primary key and check if it equal what we passed
      
        

from flaskblog import routes
