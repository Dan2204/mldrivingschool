from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Email

class ContactForm(FlaskForm):
  
  first_name = StringField('First Name: * ', validators=[DataRequired()])
  last_name = StringField('Last Name: * ', validators=[DataRequired()])
  email = StringField('Email: * ', validators=[DataRequired(), Email()])
  phone = StringField('Phone: * ', validators=[DataRequired()])
  subject = StringField('Subject: ')
  details = TextAreaField('Details: * ', validators=[DataRequired()])
  # anti_bot = IntegerField('4 + 1 = ', validators=[DataRequired(), 
  #                                                 NumberRange(min=5, max=5, message='Please add 4 and 1')])
  recaptcha = RecaptchaField()
  submit = SubmitField('Submit')
  