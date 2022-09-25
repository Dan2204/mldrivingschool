from ml_driving.users import bp 
from ml_driving.models import User, Review
from ml_driving.admin.forms import ImageForm
from ml_driving.users.forms import ChangeUserPasswordForm, CreateUserForm, EditUserForm
from ml_driving.core.menu_items import admin_menu
from ml_driving.core.template_options import template_options
from ml_driving.admin.form_db_process import (add_user, edit_user_details, activate_user, deactivate_user,
                                              delete_user, change_user_password)
from ml_driving.users.forms import ChangePasswordForm, ChangeUserPasswordForm
from ml_driving.admin.notifications import send_notification
from ml_driving.admin.process_form import format_error_form, format_general_db_error

from flask import render_template, redirect, flash, url_for, request, session
from flask_login import current_user, login_required


@bp.route("/users", methods=["GET", "POST"])
@login_required
def users():
  
  if not current_user.admin:
    flash("You need to be an Admin to view this page.")
    return redirect(url_for('admin.admin', user_id=current_user.id))
  
  users = User.query.all()
  
  template_data = {
    'image_form': ImageForm(),
    'password_form': ChangePasswordForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options
  }
  
  return render_template('user_page.html', title="Users", sub_menu=admin_menu, 
                         users=users, data=template_data)


@bp.route("/users/create-user", methods=["GET", "POST"])
@login_required
def create_user():
  
  if not current_user.admin:
    flash("You need to be an Admin to view this page.")
    return redirect(url_for('admin.admin', user_id=current_user.id))
  
  template_data = {
    'image_form': ImageForm(),
    'password_form': ChangePasswordForm(),
    'add_user_form': CreateUserForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options,
  }
  
  if template_data['add_user_form'].validate_on_submit():
    has_error = add_user(template_data['add_user_form'])    
    if has_error[0]:
      send_notification(format_error_form(template_data['add_user_form'], has_error[1]))
      flash("Error adding user, please contact admin")
    else:
      flash("New User Added.")

    return redirect(url_for('users.users'))
    
  return render_template('create_user.html', title="Create User", data=template_data)


@bp.route('/admin/edit-user/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
  
  if not current_user.admin:
    flash("You need to be an Admin to view this page.")
    return redirect(url_for('admin.admin', user_id=current_user.id))
  
  user = User.query.get_or_404(user_id)
  template_data = {
    'edit_user_form': EditUserForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options,
    'edit_page_details': {
      'type': 'User',
      'back_title': 'back to users',
      'back_url': 'users.users',
      'form_page': "_edit_user.html",
    },
  }
  
  if template_data['edit_user_form'].validate_on_submit():
    has_error = edit_user_details(template_data['edit_user_form'], user)
    if has_error[0]:
      send_notification(format_error_form(template_data['edit_user_form'], has_error[1]))
      flash_message = "Error processing user, contact admin"
    else:
      session['name'] = ""
      session['email'] = ""
      flash_message = "User Updated."
    flash(flash_message)
    return redirect(url_for('users.users'))
  elif request.method == "GET":
    template_data['edit_user_form'].name.data = user.name
    template_data['edit_user_form'].email.data = user.email
    template_data['edit_user_form'].admin.data = user.admin
    session['name'] = user.name
    session['email'] = user.email 
  return render_template('edit_page.html', title=f"Edit: {user.name}", data=template_data,
                         user=user)
    
 
@bp.route('/admin/close-user/<user_id>', methods=['GET', 'POST'])
@login_required
def close_user(user_id):   
  
    if not current_user.admin:
      flash("You need to be an Admin to view this page.")
      return redirect(url_for('admin.admin', user_id=current_user.id))
  
    user = User.query.get_or_404(user_id)
    
    has_error = deactivate_user(user_id)
    if has_error[0]:
      send_notification(format_general_db_error("Deactivating User", has_error[1]))
      flash_message = "Error Deactivating, Admin have been informed"
    else:
      flash_message = f"{user.name} has been deactivated"
    flash(flash_message)
    
    return redirect(url_for('users.users'))
 
 
@bp.route('/admin/reactivate-user/<user_id>', methods=['GET', 'POST'])
@login_required
def reactivate_user(user_id): 
  
    if not current_user.admin:
      flash("You need to be an Admin to view this page.")
      return redirect(url_for('admin.admin', user_id=current_user.id))
  
    user = User.query.get_or_404(user_id)
    
    has_error = activate_user(user_id)
    if has_error[0]:
      send_notification(format_general_db_error("Activating User", has_error[1]))
      flash_message = "Error Activating, Admin have been informed"
    else:
      flash_message = f"{user.name} has been reactivated"
    flash(flash_message)
    
    return redirect(url_for('users.users'))


@bp.route('/admin/delete-user/<user_id>', methods=['GET', 'POST'])
@login_required
def remove_user(user_id):
  
  has_error = delete_user(user_id)
  if has_error[0]:
    send_notification(format_general_db_error("Deleteing User", has_error[1]))
    flash_message = "Error deleteing user, Admin have been informed"
  else:
    flash_message = "User Deleted"
  flash(flash_message)
  
  return redirect(url_for('users.users'))
  

@bp.route('/admin/edit-user-password/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user_password(user_id):
  
  if not current_user.admin:
    flash("You need to be an Admin to view this page.")
    return redirect(url_for('admin.admin', user_id=current_user.id))
  
  user = User.query.get_or_404(user_id)
  template_data = {
    'user_password_form': ChangeUserPasswordForm(),
    'has_new_reviews': Review.query.filter_by(active=False).all(),
    'options': template_options,
    'edit_page_details': {
      'type': 'Password',
      'back_title': 'back to users',
      'back_url': 'users.users',
      'form_page': "_change_user_password.html",
    },
  }
  
  if template_data['user_password_form'].validate_on_submit():
    has_error = change_user_password(template_data['user_password_form'], user)
    if has_error[0]:
      send_notification(format_error_form(template_data['user_password_form'], has_error[1]))
      flash_message = "Error processing request, contact admin"
    else:
      flash_message = "User Updated."
    flash(flash_message)
    return redirect(url_for('users.users'))
  
  return render_template('edit_page.html', title=f"Edit: {user.name}", data=template_data,
                         user=user)
    
 