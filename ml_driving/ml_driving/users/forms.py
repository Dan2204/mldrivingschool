from flask import session
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from ml_driving.models import User
 

class ChangePasswordForm(FlaskForm):
  
  current_password = PasswordField('Current Password: ', validators=[DataRequired()])
  new_password = PasswordField('New Password: ', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(),
                                                                     EqualTo('new_password')])
  submit_password = SubmitField('Change Password')
  

class ChangeUserPasswordForm(FlaskForm):
  
  new_password = PasswordField('New Password: ', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(),
                                                                     EqualTo('new_password')])
  submit_password = SubmitField('Change Password')
  
  
class CreateUserForm(FlaskForm):
  
  name = StringField('Name: ', validators=[DataRequired()])
  email = StringField('Email: ', validators=[DataRequired(), Email()])
  password = PasswordField('Password: ', validators=[DataRequired()])
  password_conf = PasswordField('Confirm Password: ', validators=[
                                  DataRequired(), EqualTo('password',
                                      message='Passwords must match!')])
  admin = BooleanField('Make Admin: ')
  submit_create = SubmitField('Create')
  
  def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError('That name is already in use.')

  def validate_email(self, email):
      email = User.query.filter_by(email=email.data).first()
      if email is not None:
          raise ValidationError('That email is already in use.')


class EditUserForm(FlaskForm):
  
    name = StringField('Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    admin = BooleanField('Make Admin: ')
    submit_update = SubmitField('Save Changes')

    # --> Form Validation <--
    def validate_name(self, name):
        if name.data != session['name']:
            if User.query.filter_by(name=name.data).first():
                raise ValidationError('That name is already in use.')

    def validate_email(self, email):
        if email.data != session['email']:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('That email is already in use.')