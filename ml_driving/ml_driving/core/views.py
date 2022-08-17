from ml_driving.core import bp

from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required


@bp.route('/')
def home():
  return render_template('home.html', title="Home")


@bp.route('/about')
def about():
  return render_template('about.html', title="About")


@bp.route('/plans/standard')
def standard():
  
  sub_menu = {
    "option1": {
      "option": "Standard",
      "link": "core.standard",
    },
    "option2": {
      "option": "Intensive",
      "link": "core.intensive",
    },
    "option3": {
      "option": "Refresher",
      "link": "core.refresher",
    },
  }
  
  return render_template('plan_std.html', title="Standard", sub_menu=sub_menu)


@bp.route('/plans/intensive')
def intensive():
  
  sub_menu = {
    "option1": {
      "option": "Standard",
      "link": "core.standard",
    },
    "option2": {
      "option": "Intensive",
      "link": "core.intensive",
    },
    "option3": {
      "option": "Refresher",
      "link": "core.refresher",
    },
  }
  
  return render_template('plan_intense.html', title="Intensive", sub_menu=sub_menu)


@bp.route('/plans/refresher')
def refresher():
  
  sub_menu = {
    "option1": {
      "option": "Standard",
      "link": "core.standard",
    },
    "option2": {
      "option": "Intensive",
      "link": "core.intensive",
    },
    "option3": {
      "option": "Refresher",
      "link": "core.refresher",
    },
  }
  
  return render_template('plan_refresher.html', title="Refresher", sub_menu=sub_menu)


@bp.route('/journey/eligibility')
def eligibility():
  
  sub_menu = {
    "option1": {
      "option": "Eligibility",
      "link": "core.eligibility",
    },
    "option2": {
      "option": "Theory",
      "link": "core.theory",
    },
    "option3": {
      "option": "Practical",
      "link": "core.practical",
    },
  }
  
  return render_template('eligibility.html', title="Eligibility", sub_menu=sub_menu)


@bp.route('/journey/theory')
def theory():
  
  sub_menu = {
    "option1": {
      "option": "Eligibility",
      "link": "core.eligibility",
    },
    "option2": {
      "option": "Theory",
      "link": "core.theory",
    },
    "option3": {
      "option": "Practical",
      "link": "core.practical",
    },
  }
  
  return render_template('theory.html', title="Theory", sub_menu=sub_menu)


@bp.route('/journey/practical')
def practical():
  
  sub_menu = {
    "option1": {
      "option": "Eligibility",
      "link": "core.eligibility",
    },
    "option2": {
      "option": "Theory",
      "link": "core.theory",
    },
    "option3": {
      "option": "Practical",
      "link": "core.practical",
    },
  }
  
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

