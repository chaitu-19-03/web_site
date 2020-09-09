from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app1.models import user

class reg_form(FlaskForm):
    username = StringField('username'
        ,validators=[DataRequired(),Length(min = 5,max=16)])
    email = StringField('email',validators=[DataRequired()])
    password = StringField('password',validators=[DataRequired()])
    confirm_pass = StringField('Confirm_Password',
        validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Sign up')

    def validate_username(self,username):
        userx = user.query.filter_by(username = username.data).first()
        if userx:
            raise ValidationError('username already taken')

        def validate_email(self,email):
            emailx = user.query.filter_by(email = email.data).first()
            if userx:
                raise ValidationError('email already taken')


class login_form(FlaskForm):

    email = StringField('email',validators=[DataRequired()])
    password = StringField('Password',validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField('log in')

class update_form(FlaskForm):
    username = StringField('username'
        ,validators=[DataRequired(),Length(min = 5,max=16)])
    email = StringField('email',validators=[DataRequired()])
    pro_pic = FileField('update profile picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('update')

    def validate_username(self,username):
        if username.data != current_user.username :
            userx = user.query.filter_by(username = username.data).first()
            if userx:
                raise ValidationError('username already taken')

    def validate_email(self,email):
            if email.data != current_user.email :
              emailx = user.query.filter_by(email = email.data).first()
              if userx:
                    raise ValidationError('email already taken')

class request_reset_form(FlaskForm):
     email = StringField('email',validators=[DataRequired()])
     submit = SubmitField('request reset')

     def validate_email(self,email):
            emailx = user.query.filter_by(email = email.data).first()
            if emailx is None:
                raise ValidationError('email dosent exist')


class reset_password_form(FlaskForm):

    password = StringField('password',validators=[DataRequired()])
    confirm_pass = StringField('Confirm_Password',
        validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('resert password')
