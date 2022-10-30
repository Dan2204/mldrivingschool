from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Email, ValidationError
from ml_driving.models import Review

class ReviewForm(FlaskForm):
  
  name = StringField('Name: * ', validators=[DataRequired()])
  email = StringField('Email: * ', validators=[DataRequired(), Email()])
  details = TextAreaField('Your review: * ', validators=[DataRequired()])
  # anti_bot = IntegerField('4 + 1 = ', validators=[DataRequired(), 
  #                                                 NumberRange(min=5, max=5, message='Please add 4 and 1')])
  recaptcha = RecaptchaField()
  submit = SubmitField('Submit')
  
  def validate_name(self, name):
    if Review.query.filter_by(name=name.data).first():
      raise ValidationError('Please use a different name.')
  