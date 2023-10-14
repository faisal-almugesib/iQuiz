from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from datetime import date


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2,max=20)])#not empty and 2<=length<=20 
    
    email = StringField('Email',
                        validators=[DataRequired(), Email()])#not here i delete the email check function because of an error
    
    password = PasswordField('Password',
                            validators=[DataRequired()])
    
    confirm_password =PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])
    
    submit =SubmitField('Sign Up')


class LoginForm(FlaskForm):    
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2,max=20)])#not empty and here i delete the username check function because of an error
    
    password = PasswordField('Password',
                            validators=[DataRequired()])
    
    remember = BooleanField('Remember Me') # cookies

    submit =SubmitField('Login')


class DeleteForm(FlaskForm):    
    #username = StringField('Username',
    #                       validators=[DataRequired(), Length(min=2,max=20)])#not empty and here i delete the username check function because of an error
    
    password = PasswordField('Password',
                            validators=[DataRequired()])

    submit =SubmitField('Delete')


class EditNameForm(FlaskForm):    

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2,max=20)])
    
    submit =SubmitField('Edit')

class EditEmailForm(FlaskForm):    

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    submit =SubmitField('Edit') 

class ChangePassword(FlaskForm):   

    oldpassword = PasswordField('Password',
                            validators=[DataRequired()])
    
    newpassword = PasswordField('Password',
                            validators=[DataRequired()])
    
    confirm_newpassword =PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('newpassword')])
    
    submit =SubmitField('Change')


def validate_date(form, field):
    if field.data < date.today():
        raise ValidationError('Date cannot be in the past.')

class AddDateForm(FlaskForm):   

    date = DateField('Date',
                            validators=[DataRequired(), validate_date])
    course = StringField('Course',
                           validators=[DataRequired()]) 
    addDate =SubmitField('Add date')






'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
'''