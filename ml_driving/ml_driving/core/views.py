import datetime
from ml_driving.core import bp
from ml_driving.core.form import ContactForm
from ml_driving.models import Contact, ContactNote, Image
from ml_driving.admin.process_form import format_contact_form, format_error_form
from ml_driving.admin.notifications import send_notification
from ml_driving.admin.form_db_process import add_contact
from ml_driving.core.menu_items import price_menu, journey_menu, review_menu

from flask import render_template, redirect, url_for, flash, request, Response


@bp.route('/robots.txt')
def robots_txt():
    r = Response(response="User-Agent: *\nDisallow:/admin/\nDisallow:/reviews/approve\n" 
                 "Disallow:/reviews/delete\nDisallow:/users/\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@bp.route('/', methods=['GET', 'POST'])
def home():
  
  form = ContactForm()
  back = request.referrer
  
  if form.validate_on_submit():
    has_error = add_contact(form)    
    if has_error[0]:
      send_notification(format_error_form(form, has_error[1]))
    else: 
      if send_notification(format_contact_form(form)):
        flash("Message Sent, Please wait for reply.")
      else:
        flash("Error sending message, please call MLDS")
    return redirect(back)
  
  return render_template('home.html', title="Home", form=form, form_title="Get in touch:" )


@bp.route('/about')
def about():
  return render_template('about.html', title="About")


@bp.route('/plans/standard', methods=['GET', 'POST'])
def standard():
  
  form = ContactForm()
  back = request.referrer
  sub_menu = price_menu
  
  if form.validate_on_submit():
    has_error = add_contact(form)    
    if has_error[0]:
      send_notification(format_error_form(form, has_error[1]))
    else: 
      if send_notification(format_contact_form(form)):
        flash("Message Sent, Please wait for reply.")
      else:
        flash("Error sending message, please call MLDS")
    return redirect(back)
  
  return render_template('plan_std.html', title="Standard", sub_menu=sub_menu, form=form)


@bp.route('/plans/intensive', methods=['GET', 'POST'])
def intensive():
  
  form = ContactForm()
  back = request.referrer
  sub_menu = price_menu
  
  if form.validate_on_submit():
    has_error = add_contact(form)    
    if has_error[0]:
      send_notification(format_error_form(form, has_error[1]))
    else: 
      if send_notification(format_contact_form(form)):
        flash("Message Sent, Please wait for reply.")
      else:
        flash("Error sending message, please call MLDS")
    return redirect(back)
  
  return render_template('plan_intense.html', title="Intensive", sub_menu=sub_menu, 
                         form=form, form_title="Ask a question:")


@bp.route('/plans/refresher', methods=['GET', 'POST'])
def refresher():
  
  form = ContactForm()
  back = request.referrer
  sub_menu = price_menu
  
  if form.validate_on_submit():
    has_error = add_contact(form)    
    if has_error[0]:
      send_notification(format_error_form(form, has_error[1]))
    else: 
      if send_notification(format_contact_form(form)):
        flash("Message Sent, Please wait for reply.")
      else:
        flash("Error sending message, please call MLDS")
    return redirect(back)
  
  return render_template('plan_refresher.html', title="Refresher", 
                         sub_menu=sub_menu, form=form, form_title="Ask a question:")


@bp.route('/journey/eligibility')
def eligibility():
  
  sub_menu = journey_menu
  
  return render_template('eligibility.html', title="Eligibility", sub_menu=sub_menu)


@bp.route('/journey/theory')
def theory():
  
  sub_menu = journey_menu
  
  return render_template('theory.html', title="Theory", sub_menu=sub_menu)


@bp.route('/journey/practical')
def practical():
  
  sub_menu = journey_menu
  
  return render_template('practical.html', title="Practical", sub_menu=sub_menu)


@bp.route('/useful-info')
def useful_info():
  return render_template('links.html', title="Useful Links")


@bp.route('/faqs')
def faqs():
  return render_template('faq.html', title="FAQ's")


@bp.route('/gallery')
def gallery():
  
  images = Image.query.all()
  
  return render_template('gallary.html', title="Gallery", sub_menu=review_menu, images=images)


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
  
  form = ContactForm()
  back = request.referrer
  
  if form.validate_on_submit():
    has_error = add_contact(form)    
    if has_error[0]:
      send_notification(format_error_form(form, has_error[1]))
    else: 
      if send_notification(format_contact_form(form)):
        flash("Message Sent, Please wait for reply.")
      else:
        flash("Error sending message, please call MLDS")
    return redirect(back)
  
  return render_template('contact.html', title="Contact", form=form, form_title="Ask a question:")


