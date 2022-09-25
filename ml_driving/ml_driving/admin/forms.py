from flask import session
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed

from ml_driving.models import Contact


class ImageForm(FlaskForm):
  
  image = FileField('Add Image: ', validators=[
                    FileAllowed(['jpg', 'png', 'jpeg']), DataRequired()])
  pass_date = DateField('Pass Date: ', format='%Y-%m-%d', validators=[DataRequired()])
  submit_image = SubmitField('Upload')


class EditImageForm(FlaskForm):
  
  image = FileField('Add Image: ', validators=[
                    FileAllowed(['jpg', 'png', 'jpeg'])])
  pass_date = DateField('Pass Date: ', format='%Y-%m-%d', validators=[DataRequired()])
  submit_image = SubmitField('Confirm')
  
  
class LoginForm(FlaskForm):
  
  email = StringField('Email: ', validators=[DataRequired(), Email()])
  password = PasswordField('Password: ', validators=[DataRequired()])
  submit_login = SubmitField('Login')
  

class NoteForm(FlaskForm):
  
  note = StringField('Note:', validators=[DataRequired()])
  submit_note = SubmitField('Add Note')
  
  
class EditContactForm(FlaskForm):
  
  name = StringField('Name:', validators=[DataRequired()])
  email = StringField('Email:', validators=[DataRequired()])
  phone = StringField('Phone:', validators=[DataRequired()])
  submit_edit = SubmitField('Update')
  
  def validate_email(self, email):
        if email.data != session['current_contact']:
            if Contact.query.filter_by(email=email.data).first():
                raise ValidationError('That email has already been used.')
