from ml_driving import db
from ml_driving.models import Contact, ContactNote, Review, User, UserActivity, Image
from ml_driving.admin.upload_img_handler import add_gallery_image

from flask_login import current_user

def add_contact(form):
  contact = Contact.query.filter_by(email=form.email.data).first()
  if contact:
    new_contact = False
    note_subject = ContactNote(note_type='Website Form - Subject', 
                               note=form.subject.data, contact=contact)
    note_details = ContactNote(note_type='Website Form - Message', 
                               note=form.details.data, contact=contact)
  else:  
    name = f"{form.first_name.data} {form.last_name.data}"
    new_contact = Contact(name=name, email=form.email.data, phone=form.phone.data)
    note_subject = ContactNote(note_type='Website Form - Subject', 
                               note=form.subject.data, contact=new_contact)
    note_details = ContactNote(note_type='Website Form - Message', 
                               note=form.details.data, contact=new_contact)
  try:
    if new_contact:
      db.session.add(new_contact)
    db.session.add(note_subject)
    db.session.add(note_details)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]
  

def edit_contact_details(form, contact_id):
  contact = Contact.query.get_or_404(contact_id)
  new_activity = UserActivity(activity=f"Changed details for {contact.name}: {contact.email} - {contact.phone}", 
                              activity_user=current_user)
  try:
    contact.name = form.name.data
    contact.email = form.email.data
    contact.phone = form.phone.data
    db.session.add(new_activity)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]
  
  
def deactivate_contact(contact_id):
  contact = Contact.query.get_or_404(contact_id)
  new_activity = UserActivity(activity=f"Deactivated Contact: {contact.name} - {contact.email} - {contact.phone}", 
                              activity_user=current_user)
  if contact.active:
    try:
      contact.active = False
      db.session.add(new_activity)
      db.session.commit()
    except Exception as e:
      return [True, e]
  return [False, None]
  
  
def activate_contact(contact_id):
  contact = Contact.query.get_or_404(contact_id)
  new_activity = UserActivity(activity=f"Reactivated: {contact.name} - {contact.email} - {contact.phone}", 
                              activity_user=current_user)
  if not contact.active:
    try:
      contact.active = True
      db.session.add(new_activity)
      db.session.commit()
    except Exception as e:
      return [True, e]
  return [False, None]
  

def delete_contact(contact_id):
  contact = Contact.query.get_or_404(contact_id)
  new_activity = UserActivity(activity=f"Deleted Contact: {contact.name}", activity_user=current_user)
  try:
    for note in contact.notes:
      db.session.delete(note)
    for review in contact.reviews:
      db.session.delete(review)
    db.session.add(new_activity)
    db.session.delete(contact)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]


def add_contact_note(form, contact_id):
  contact = Contact.query.get_or_404(contact_id)
  new_note = ContactNote(note=form.note.data, contact=contact, note_user=current_user)
  new_activity = UserActivity(activity=f"Added note for {contact.name}: {new_note.note}", 
                              activity_user=current_user)
  try:
    db.session.add(new_note)
    db.session.add(new_activity)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]
  

def delete_contact_note(note_id):
  note = ContactNote.query.get_or_404(note_id)
  new_activity = UserActivity(activity=f"Deleted note from: {note.contact.name}", activity_user=current_user)
  try:
    db.session.add(new_activity)
    db.session.delete(note)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]
  
  
def add_review(form):
  contact = Contact.query.filter_by(email=form.email.data).first()
  add_contact = contact if contact else None
  new_review = Review(name=form.name.data, email=form.email.data, 
                      review=form.details.data, contact=add_contact)
  try:
    db.session.add(new_review)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]


def update_review(review_id):
  review = Review.query.get_or_404(review_id)
  review.active = True
  new_activity = UserActivity(activity=f"Approved Review: {review.name} - {review.email}", 
                              activity_user=current_user)
  try:
    db.session.add(new_activity)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]


def review_deletion(review_id):
  review = Review.query.get_or_404(review_id)
  delete_permanently = not review.active
  review.active = False
  try:
    if delete_permanently:
      activity=f"Review Deleted: {review.name} - {review.email}"
      db.session.delete(review)
    else:
      activity=f"Review moved to approvals: {review.name} - {review.email}"
    new_activity = UserActivity(activity=activity, activity_user=current_user)
    db.session.add(new_activity)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]
  
  
def add_image(form):
  image_filename = add_gallery_image(form.image.data, current_user.id,
                                       form.pass_date.data, len(Image.query.all()))
  new_image = Image(image=image_filename, pass_date=form.pass_date.data, image_user=current_user)
  activity = f'Added Image: {image_filename}'
  new_activity = UserActivity(activity=activity, activity_user=current_user)
  try:
    db.session.add(new_image)
    db.session.add(new_activity)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]
  
  
def edit_images(form, image):
  if form.image.data:
    image_filename = add_gallery_image(form.image.data, current_user.id,
                                        form.pass_date.data, len(Image.query.all()))
    image.image = image_filename
  else:
    image_filename = image.image
  if image.pass_date != form.pass_date.data:
    activity_pd = " and Passdate"
  else:
    activity_pd = ""
  image.pass_date = form.pass_date.data
  activity_name = f": {image_filename}"
  activity = f'Updated Image{activity_pd}{activity_name}'
  new_activity = UserActivity(activity=activity, activity_user=current_user)
  try:
    db.session.add(new_activity)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]


def delete_img(img_id):
  image = Image.query.get_or_404(img_id)
  new_activity = UserActivity(activity=f"Deleted Image: {image.image}", activity_user=current_user)
  try:
    db.session.add(new_activity)
    db.session.delete(image)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]


def add_activity(user_activity, user):
  new_activity = UserActivity(activity=user_activity, activity_user=user)
  try:
    db.session.add(new_activity)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]
  

def change_user_password(form, user):
  if user.id == current_user.id:
    checked = user.check_password(form.current_password.data)
  else:
    checked = current_user.admin
  
  if checked:
    activity = f'Changed user password: (id => {user.id}, name => {user.name})'
    user.set_password(form.new_password.data)
    new_activity = UserActivity(activity=activity, activity_user=current_user)
    try:
      db.session.add(new_activity)
      db.session.commit()
      return[False, None]
    except Exception as e:
      return [True, e]
  else:
    return [True, "password"]
    
  
def add_user(form):
  new_user = User(name=form.name.data, email=form.email.data, 
                  password=form.password.data, admin=form.admin.data)
  new_user.created_by = current_user.id
  new_activity = UserActivity(activity=f"Created User: {new_user.name}", activity_user=current_user)
  try:
    db.session.add(new_user)
    db.session.add(new_activity)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]  
  
  
def edit_user_details(form, user):
  activity = f'Updated User: {user.name} - {user.email}'
  new_activity = UserActivity(activity=activity, activity_user=current_user)
  try:
    user.name = form.name.data
    user.email = form.email.data
    user.admin = form.admin.data
    db.session.add(new_activity)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]
  
  
def deactivate_user(user_id):
  user = User.query.get_or_404(user_id)
  new_activity = UserActivity(activity=f"Deactivated user: {user.name} - {user.email}", 
                              activity_user=current_user)
  if user.active:
    try:
      user.active = False
      db.session.add(new_activity)
      db.session.commit()
    except Exception as e:
      return [True, e]
  return [False, None]
  
  
def activate_user(user_id):
  user = User.query.get_or_404(user_id)
  new_activity = UserActivity(activity=f"Reactivated: {user.name} - {user.email}", 
                              activity_user=current_user)
  if not user.active:
    try:
      user.active = True
      db.session.add(new_activity)
      db.session.commit()
    except Exception as e:
      return [True, e]
  return [False, None]
  

def delete_user(user_id):
  user = User.query.get_or_404(user_id)
  new_activity = UserActivity(activity=f"Deleted User: {user.name}", activity_user=current_user)
  try:
    for activity in user.activities:
      db.session.delete(activity)
    db.session.add(new_activity)
    db.session.delete(user)
    db.session.commit()
    return [False, None]
  except Exception as e:
    return [True, e]