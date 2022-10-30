from ml_driving import db
from ml_driving.reviews import bp
from ml_driving.models import Review
from ml_driving.reviews.form import ReviewForm
from ml_driving.core.menu_items import review_menu
from ml_driving.admin.process_form import format_review_form, format_error_form, format_general_db_error
from ml_driving.admin.form_db_process import add_review, update_review, review_deletion
from ml_driving.admin.notifications import send_notification

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required


@bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
  
  form = ReviewForm()
  back = request.referrer
  reviews = Review.query.filter_by(active=True).all()
  
  if form.validate_on_submit():
    has_error = add_review(form)
    if has_error[0]:
      send_notification(format_error_form(form, has_error[1]))
    else:
      if send_notification(format_review_form(form)):
        flash_message = "Review Submitted For Approval"
      else:
        flash_message = "Error sending review, please call MLDS"
    flash(flash_message)
    return redirect(back)
  
  return render_template('reviews.html', title="Reviews", form=form, reviews=reviews, 
                         sub_menu=review_menu)
  
  
@bp.route('/reviews/approve/<review_id>', methods=['GET', 'POST'])
@login_required
def approve_review(review_id):
  
  has_error = update_review(review_id)
  if has_error[0]:
    send_notification(format_general_db_error("Approving Review", has_error[1]))
    flash_message = "Error updating, Admin have been informed"
  else:
    flash_message = "Review Approved"
  flash(flash_message)
  
  return redirect(request.referrer)
  
  
@bp.route('/reviews/delete/<review_id>', methods=['GET', 'POST'])
@login_required
def delete_review(review_id):
  
  has_error = review_deletion(review_id)
  if has_error[0]:
    send_notification(format_general_db_error("Deleteing Review", has_error[1]))
    flash_message = "Error deleteing, Admin have been informed"
  else:
    flash_message = "Review Moved/Deleted"
  flash(flash_message)
  
  return redirect(request.referrer)