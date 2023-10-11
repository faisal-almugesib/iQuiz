from flask import render_template,url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm, DeleteForm, EditEmailForm, EditNameForm, ChangePassword
from flaskblog.modelss import User, Post
from flaskblog import db
from flask_login import login_user, login_required, logout_user, current_user



'''
posts = [ {'author': 'Faisal',
           'title': 'Flask Training',
           'content':'WhAt ThE FuCk iS GoInG oN',
           'date_posted': 'September 12, 2023'}
           
           ,


           {'author': 'PanDaa',
           'title': 'MeoW',
           'content':'HeLLo \'-\'',
           'date_posted': 'September 12, 2023'}]
'''

@app.route("/")
@login_required
def home():
    return render_template('index.html', user=current_user)  #posts=posts 

@app.route("/about")
def about():
    return render_template('flaskblog\Bikin\templates\index.html',title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email= form.email.data, username=form.username.data, password=form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        user1 = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Email already exist', 'danger')
        
        elif user1:
            flash('Username already exist', 'danger')

        else:    
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(f'Account created for {form.username.data}!',category='success')
            return redirect(url_for('home'))
    return render_template('register.html',title='Register', form=form, user=current_user)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()#by using this we retrive from database the first user with email = email got from login page

        if user: #if there is user we get from previous query it will be true
            if user.password == form.password.data:
                flash('You have been logged in !', 'success')
                login_user(user, remember=True) # work like the session or cookie it make user status to login and remember it until he logout or flask server restart
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again', 'danger')
        else:
            flash('Username does not exist.', 'danger')
    return render_template('login.html',title='Login', form=form, user=current_user)


@app.route('/logout')
@login_required # this to make sure you cant acces this page unless you are login
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account", methods=['GET','POST'])

def account():
    form = DeleteForm()
    form1 = EditNameForm()
    form2 = EditEmailForm()
    form3 = ChangePassword()

    
    if form1.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user1 = User.query.filter_by(username=form1.username.data).first()
        
        if user1:
            flash('Username already exist', 'danger')

        else:
            user.username = form1.username.data
            db.session.commit()
            flash('Your Username has been Changed !', 'success')



    if form2.validate_on_submit():
        user1 = User.query.filter_by(email=form2.email.data).first()
        
        if user1:
            flash('Email already exist', 'danger')

        else:
            user = User.query.filter_by(email=current_user.email).first()
            user.email = form2.email.data
            db.session.commit()
            flash('Your Email has been Changed !', 'success')


    if form3.validate_on_submit():
        if current_user.password == form3.oldpassword.data:
            #if form3.newpassword.data == form3.confirm_newpassword.data:
                user = User.query.filter_by(username=current_user.username).first()
                user.password = form3.newpassword.data
                db.session.commit()
                flash('Your password has been Changed !', 'success')

           # else:
            #    flash('The confirm new password doesn\'t match the new password , try again', 'danger')

        else:
            flash('Incorrect password, try again', 'danger')









    if form.validate_on_submit():
        if current_user.password == form.password.data:
            flash('Your account has been Deleted !', 'success')
            user = User.query.filter_by(username=current_user.username).first()
            db.session.delete(user)
            db.session.commit()
            #logout_user()
            return redirect(url_for('register'))
        else:
            flash('Incorrect password, try again', 'danger')


    return render_template('account.html',title='Account', form = form, form1 = form1, form2 = form2, form3 = form3, user = current_user)


@app.route("/quiz", methods=['GET','POST'])
@login_required
def quiz():
    return render_template('quiz.html', user=current_user)