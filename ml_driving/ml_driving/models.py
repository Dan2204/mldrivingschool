from datetime import datetime
from ml_driving import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


class User(db.Model, UserMixin):
  
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), nullable=False, unique=True, index=True)
  email = db.Column(db.String(64), nullable=False, unique=True, index=True)
  admin = db.Column(db.Boolean, nullable=False, default=False)
  active = db.Column(db.Boolean, nullable=False, default=True)
  creation_date = db.Column(db.DateTime, default=datetime.utcnow)
  created_by = db.Column(db.Integer, default=0)
  password_hash = db.Column(db.String(128), nullable=False)
  
  contact_notes = db.relationship('ContactNote', backref='note_user', lazy='dynamic')
  images = db.relationship('Image', backref='image_user', lazy='dynamic')
  activities = db.relationship('UserActivity', backref='activity_user', lazy='dynamic')
  
  def __init__(self, name, email, password, admin=False):
    self.name = name
    self.email = email
    self.admin = admin
    self.password_hash = generate_password_hash(password)
    
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  
class UserActivity(db.Model):
  
  __tablename__ = 'user_activity'
  
  id = db.Column(db.Integer, primary_key=True)
  activity = db.Column(db.String(128), nullable=False, index=True)
  creation_date = db.Column(db.DateTime, default=datetime.utcnow)
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  
  
class Contact(db.Model):
  
  __tablename__ = 'contacts'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), nullable=False, unique=True, index=True)
  email = db.Column(db.String(64), nullable=False, unique=True, index=True)
  phone = db.Column(db.String(64), nullable=False, unique=True, index=True)
  active = db.Column(db.Boolean, nullable=False, default=True)
  creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
  notes = db.relationship('ContactNote', backref='contact', lazy='dynamic')
  reviews = db.relationship('Review', backref='contact', lazy='dynamic')
  
  def __init__(self, name, email, phone):
    self.name = name
    self.email = email
    self.phone = phone


class ContactNote(db.Model):
  
  __tablename__ = 'contact_notes'
  
  id = db.Column(db.Integer, primary_key=True)
  note_type = db.Column(db.String(64), nullable=False, default='General')
  note = db.Column(db.Text, nullable=False, default='Nonthing Entered')
  creation_date = db.Column(db.DateTime, default=datetime.utcnow)
  
  contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Review(db.Model):
  
  __tablename__ = 'reviews'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), nullable=False, unique=True, index=True)
  email = db.Column(db.String(64), nullable=False, index=True)
  review = db.Column(db.Text, nullable=False)
  active = db.Column(db.Boolean, nullable=False, default=False)
  creation_date = db.Column(db.DateTime, default=datetime.utcnow)
  
  contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    

class Image(db.Model):
  
  __tablename__ = 'images'
  
  id = db.Column(db.Integer, primary_key=True)
  image = db.Column(db.String(64), nullable=False, default='')
  pass_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  creation_date = db.Column(db.DateTime, default=datetime.utcnow)
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

      