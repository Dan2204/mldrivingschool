from ml_driving.core import bp
from ml_driving.core.form import ContactForm
from ml_driving.core.process_form import process_form
from ml_driving.core.menu_items import price_menu, journey_menu

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required


@bp.route('/')
def home():
  return render_template('home.html', title="Home")


@bp.route('/about')
def about():
  return render_template('about.html', title="About")


@bp.route('/plans/standard', methods=['GET', 'POST'])
def standard():
  
  form = ContactForm()
  back = request.referrer
  sub_menu = price_menu
  
  if form.validate_on_submit():
    if process_form(form):
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
    if process_form(form):
      flash("Message Sent, Please wait for reply.")
    else:
      flash("Error sending message, please call MLDS")
    return redirect(back)
  
  return render_template('plan_intense.html', title="Intensive", sub_menu=sub_menu, form=form)


@bp.route('/plans/refresher', methods=['GET', 'POST'])
def refresher():
  
  form = ContactForm()
  back = request.referrer
  sub_menu = price_menu
  
  if form.validate_on_submit():
    if process_form(form):
      flash("Message Sent, Please wait for reply.")
    else:
      flash("Error sending message, please call MLDS")
    return redirect(back)
  
  return render_template('plan_refresher.html', title="Refresher", sub_menu=sub_menu, form=form)


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


@bp.route('/reviews')
def reviews():
  return render_template('reviews.html', title="Reviews")


@bp.route('/gallary')
def gallary():
  return render_template('gallary.html', title="Gallary")


@bp.route('/contact')
def contact():
  return render_template('contact.html', title="Contact")


