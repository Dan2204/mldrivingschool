from ml_driving import db
from ml_driving.admin import bp
from ml_driving.models import User, Review, Image, UserActivity, Contact
from ml_driving.core.menu_items import admin_menu
from ml_driving.users.forms import ChangePasswordForm, ChangeUserPasswordForm
from ml_driving.admin.forms import ImageForm, EditImageForm, LoginForm, NoteForm, EditContactForm
from ml_driving.core.template_options import template_options
from ml_driving.admin.form_db_process import (add_image, delete_img, add_activity, delete_contact_note,
                                              change_user_password, add_contact_note, edit_contact_details,
                                              activate_contact, deactivate_contact, delete_contact, edit_images)
from ml_driving.admin.notifications import send_notification
from ml_driving.admin.process_form import format_error_form, format_general_db_error

from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required


# @bp.route('/erudite/badger/admin', methods=['GET', 'POST'])
@bp.route('/admin/<user_id>', methods=['GET', 'POST'])
@login_required
def admin(user_id=None):  
  
  if user_id is not None and current_user.admin:
    user = User.query.get_or_404(user_id)
  else:
    user = current_user
    
    
  image_form = ImageForm()
  password_form = ChangePasswordForm()
  reviews = Review.query.filter_by(active=False).order_by(Review.creation_date.desc()).all()
  activities = list(user.activities)
  
  # template_options['admin_nav'] = "profile"
  
  if session.get('password_error') == True:
    password_form.current_password.errors = tuple(['Incorrect password.'])
    session.pop('password_error', None)
  if session.get('close_modal') == 'close':
    template_options['close_modal'] = 'close'
    session.pop('close_modal', None)
  else:
    template_options['close_modal'] = None
  
  template_data = {
    'image_form': ImageForm(),
    'password_form': ChangePasswordForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options
  }

  return render_template('admin_dash.html', title=f"Admin - {user.name}", user=user, reviews=reviews,
                         sub_menu=admin_menu, data=template_data, activities=activities)
  

@bp.route('/admin/gallery', methods=['GET', 'POST'])
@login_required
def admin_gallery():
  
  password_form = ChangePasswordForm()
  
  if session.get('password_error') == True:
    password_form.current_password.errors = tuple(['Incorrect password.'])
    session.pop('password_error', None)
  if session.get('close_modal') == 'close':
    template_options['close_modal'] = 'close'
    session.pop('close_modal', None)
  else:
    template_options['close_modal'] = None
  
  template_data = {
    'image_form': ImageForm(),
    'password_form': ChangePasswordForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'images': Image.query.order_by(Image.creation_date.desc()).all(),
    'options': template_options,
  }
  
  return render_template('admin_gallery.html', title="Admin - Gallery", sub_menu=admin_menu, data=template_data)
  

@bp.route('/admin/reviews', methods=['GET', 'POST'])
@login_required
def admin_reviews():
  
  reviews_approved = Review.query.filter_by(active=True).order_by(Review.creation_date.desc()).all()
  reviews_unapproved = Review.query.filter_by(active=False).order_by(Review.creation_date.desc()).all()
  
  password_form = ChangePasswordForm()
  
  if session.get('password_error') == True:
    password_form.current_password.errors = tuple(['Incorrect password.'])
    session.pop('password_error', None)
  if session.get('close_modal') == 'close':
    template_options['close_modal'] = 'close'
    session.pop('close_modal', None)
  else:
    template_options['close_modal'] = None
  
  template_data = {
    'image_form': ImageForm(),
    'password_form': ChangePasswordForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options,
    'approved_reviews': reviews_approved,
    'unapproved_reviews': reviews_unapproved,
  }
  
  return render_template('admin_reviews.html', title="Admin - Reviews", data=template_data, sub_menu=admin_menu)
  

@bp.route('/admin/contacts', methods=['GET', 'POST'])
@login_required
def admin_contacts():
  
  password_form = ChangePasswordForm()
  
  if session.get('password_error') == True:
    password_form.current_password.errors = tuple(['Incorrect password.'])
    session.pop('password_error', None)
  if session.get('close_modal') == 'close':
    template_options['close_modal'] = 'close'
    session.pop('close_modal', None)
  else:
    template_options['close_modal'] = None
    
  template_data = {
    'image_form': ImageForm(),
    'password_form': ChangePasswordForm(),
    'note_form': NoteForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options,
  }
  
  contacts = Contact.query.all()
    
  return render_template('admin_contacts.html', title="Admin - Contacts", data=template_data, 
                         sub_menu=admin_menu, contacts=contacts)
  

@bp.route('/admin/users', methods=['GET', 'POST'])
@login_required
def admin_users():
  return render_template('admin_users.html', title="Admin - Users")


@bp.route('/admin/user/<user_id>/<page>')
@bp.route('/admin/user/<user_id>')
@login_required
def activities(user_id, page=None):
  
  activities_per_page = 20

  if user_id != current_user and current_user.admin:
    user = User.query.get_or_404(user_id)
  else:
    user = current_user
    
  activities = user.activities.order_by(UserActivity.creation_date.desc())
  if page and page.isdigit():
    page = int(page)
  else:
    page = 1  
  pages = activities.paginate(page, activities_per_page, False)
    
  return render_template('activities.html', title=f"Activity - {user.name}", user=user, 
                         options=template_options, activities=len(list(activities)), 
                         pages=pages)
  

@bp.route('/admin/edit-contact/<contact_id>', methods=['GET', 'POST'])
@login_required
def edit_contact(contact_id):
  contact = Contact.query.get_or_404(contact_id)
  template_data = {
    'edit_contact_form': EditContactForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options,
    'edit_page_details': {
      'type': 'contact',
      'back_title': 'back to contacts',
      'back_url': 'admin.admin_contacts',
      'form_page': "_edit_contact.html",
    },
  }
  if template_data['edit_contact_form'].validate_on_submit():
    has_error = edit_contact_details(template_data['edit_contact_form'], contact_id)
    if has_error[0]:
      send_notification(format_error_form(template_data['edit_contact_form'], has_error[1]))
      flash_message = "Error processing contact, contact admin"
    else:
      session['current_contact'] = ""
      flash_message = "Contact Updated."
    flash(flash_message)
    return redirect(url_for('admin.admin_contacts'))
  elif request.method == "GET":
    template_data['edit_contact_form'].name.data = contact.name
    template_data['edit_contact_form'].email.data = contact.email
    template_data['edit_contact_form'].phone.data = contact.phone
    session['current_contact'] = contact.email 
  return render_template('edit_page.html', title=f"Edit: {contact.name}", data=template_data,
                         contact=contact)
    
 
@bp.route('/admin/close-contact/<contact_id>', methods=['GET', 'POST'])
@login_required
def close_contact(contact_id): 
  
    contact = Contact.query.get_or_404(contact_id)
    
    has_error = deactivate_contact(contact_id)
    if has_error[0]:
      send_notification(format_general_db_error("Deactivating Contact", has_error[1]))
      flash_message = "Error Deactivating, Admin have been informed"
    else:
      flash_message = f"{contact.name} has been deactivated"
    flash(flash_message)
    
    return redirect(url_for('admin.admin_contacts'))
 
 
@bp.route('/admin/reactivate-contact/<contact_id>', methods=['GET', 'POST'])
@login_required
def reactivate_contact(contact_id): 
  
    contact = Contact.query.get_or_404(contact_id)
    
    has_error = activate_contact(contact_id)
    if has_error[0]:
      send_notification(format_general_db_error("Activating Contact", has_error[1]))
      flash_message = "Error Activating, Admin have been informed"
    else:
      flash_message = f"{contact.name} has been reactivated"
    flash(flash_message)
    
    return redirect(url_for('admin.admin_contacts'))


@bp.route('/admin/delete-contact/<contact_id>', methods=['GET', 'POST'])
@login_required
def remove_contact(contact_id):
  
  has_error = delete_contact(contact_id)
  if has_error[0]:
    send_notification(format_general_db_error("Deleteing Contact", has_error[1]))
    flash_message = "Error deleteing contact, Admin have been informed"
  else:
    flash_message = "Contact Deleted"
  flash(flash_message)
  
  return redirect(url_for('admin.admin_contacts'))


@bp.route('/admin/add-note/', methods=['GET', 'POST'])
@login_required
def add_note():
  
  template_data = {
    'image_form': ImageForm(),
    'note_form': NoteForm(),
    'password_form': ChangePasswordForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options
  }
  template_data['options']['admin_nav'] = "image_upload"
  print(">>>>>>>>>>Contact id:")
  print(request.form['contact_id'])
  
  # IMAGE FORM VALIDATION
  if template_data['note_form'].validate_on_submit():
    print(request.form['contact_id'])
    contact_id = int(request.form['contact_id'])
    has_error = add_contact_note(template_data['note_form'], contact_id)
    if has_error[0]:
      send_notification(format_error_form(template_data['note_form'], has_error[1]))
      flash_message = "Error processing note, conact admin"
      session['upload_error'] = True
    else:
      flash_message = "Note added."
      session['close_modal'] = "close"
    flash(flash_message)
    return redirect(url_for('admin.admin_contacts'))

  else:
    return redirect(url_for('admin.admin_contacts'))
  

@bp.route('/admin/delete-note/<note_id>', methods=['GET', 'POST'])
@login_required
def delete_note(note_id):
  
  has_error = delete_contact_note(note_id)
  if has_error[0]:
    send_notification(format_general_db_error("Deleteing Image", has_error[1]))
    flash_message = "Error deleteing, Admin have been informed"
  else:
    flash_message = "Note Deleted"
  flash(flash_message)
  
  return redirect(url_for('admin.admin_contacts'))
  
  
@bp.route('/admin/add-image', methods=['GET', 'POST'])
@login_required
def add_images():
  
  template_data = {
    'image_form': ImageForm(),
    'password_form': ChangePasswordForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options
  }
  template_data['options']['admin_nav'] = "image_upload"
  
  # IMAGE FORM VALIDATION
  if template_data['image_form'].validate_on_submit():
    has_error = add_image(template_data['image_form'])
    if has_error[0]:
      send_notification(format_error_form(template_data['image_form'], has_error[1]))
      flash_message = "Error processing Image, conact admin"
      session['upload_error'] = True
    else:
      flash_message = "Image added to gallery"
      session['close_modal'] = "close"
    flash(flash_message)
    
    return redirect(url_for('core.gallery'))

  else:
    return redirect(url_for('admin.admin', user_id=current_user.id))
  

@bp.route('/admin/edit-image/<image_id>', methods=['GET', 'POST'])
@login_required
def edit_image(image_id):
  
  image = Image.query.get_or_404(image_id)
  
  template_data = {
    'image_form': EditImageForm(),
    'options': template_options,
    'edit_page_details': {
      'type': 'Image',
      'back_title': 'back to gallery',
      'back_url': 'admin.admin_gallery',
      'form_page': "_edit_image.html",
    },
  }
  
  if template_data['image_form'].validate_on_submit():
    print('VALID FORM SUBMITTED')
    has_error = edit_images(template_data['image_form'], image)
    if has_error[0]:
      send_notification(format_error_form(template_data['image_form'], has_error[1]))
      flash_message = "Error updating image, conact admin"
    else:
      flash_message = "Image Updated."
    flash(flash_message)
    return redirect(url_for('admin.admin_gallery'))
  
  elif request.method == "GET":
    template_data['image_form'].image.data = image.image
    template_data['image_form'].pass_date.data = image.pass_date
    
  return render_template('edit_page.html', title=f"Edit: {image.image}", data=template_data,
                         image=image)


@bp.route('/admin/delete-image/<img_id>', methods=['GET', 'POST'])
@login_required
def delete_image(img_id):
  
  has_error = delete_img(img_id)
  if has_error[0]:
    send_notification(format_general_db_error("Deleteing Image", has_error[1]))
    flash_message = "Error deleteing, Admin have been informed"
  else:
    flash_message = "Image Deleted"
  flash(flash_message)
  
  return redirect(url_for('admin.admin_gallery'))
  
  
@bp.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
 
  user = current_user
  password_form = ChangePasswordForm()
  template_options['admin_nav'] = "change_password"
  
  # PASSWORD CHANGE VALIDATION
  if password_form.validate_on_submit():
    has_error = change_user_password(password_form, user)
    if has_error[0]:
      if has_error[1] == 'password':
        flash_message = "Incorect Password"
        session['modal_error'] = 'password'
      else:
        send_notification(format_error_form(password_form, has_error[1]))
        flash_message = "Error processing password, conact admin"
    else:
      flash_message = f"Password changed for {user.name}"
      session['close_modal'] = "close"
    flash(flash_message)
  return redirect(url_for('admin.admin', user_id=current_user.id))


@bp.route('/erudite/badger/admin/login', methods=['GET', 'POST'])
def login():
  
  if current_user.is_authenticated:
    return redirect(url_for('admin.admin', user_id=current_user.id))
  
  if not User.query.all():
    new_user = User(name="admin", email="admin@admin.com", password='1234', admin=True)
    db.session.add(new_user)
    db.session.commit()
    
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user.active:
      if user is None or not user.check_password(form.password.data):
          flash('Invalid email or password')
          return redirect(url_for('admin.login'))
      if not user.active:
          flash("Sorry, account suspended, please contact admin.")
          return redirect(url_for('admin.login'))
      login_user(user)
      has_error = add_activity("Logging in", user)
      if has_error[0]:
        send_notification(format_general_db_error("Adding Activity - Logging in", has_error[1]))
        flash_message = "Database Error. Admin have been informed."
      else:
        flash_message = f'{user.name} is now logged in.'
      flash(flash_message)
      next = request.args.get('next')
      if not next or url_parse(next).netloc != '':
          next = url_for('admin.admin', user_id=current_user.id)
    else:
      flash("Please contact admin.")
      return redirect(url_for('admin.login'))
    return redirect(next)
  
  return render_template('login.html', title="Login", form=form)


@bp.route('/logout')
@login_required
def logout():
    has_error = add_activity("Logged out", current_user)
    if has_error[0]:
      send_notification(format_general_db_error("Adding Activity - Logging out", has_error[1]))
    logout_user()
    flash('Logged out')
    return redirect(url_for('core.home'))
  

