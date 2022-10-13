from flask import render_template
from flask_login import current_user

from ml_driving import db
from ml_driving.errors import bp
from ml_driving.admin.notifications import send_notification
from ml_driving.admin.form_db_process import add_activity
from ml_driving.admin.process_form import format_error_form, format_general_db_error


@bp.app_errorhandler(403)
def error_403(error):
    return render_template('errors/errors.html', title="403", system_error=error), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/errors.html', title="404", system_error=error), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    try:
      if current_user:
        has_error = add_activity("500 Error", current_user)
        if has_error[0]:
          send_notification(format_general_db_error(f"Adding Activity - 500: {current_user.name}", has_error[1]))
    except Exception as e:
      print()
      send_notification(format_general_db_error(f"Addidng Activity For => 500 Error:", e))
      
    send_notification(format_general_db_error(f"System 500 Error:", error))
    return render_template('errors/errors.html', title="500", system_error=error), 500


@bp.app_errorhandler(501)
def db_error(error):
    try:
      if current_user:
        has_error = add_activity("501 Error", current_user)
        if has_error[0]:
          send_notification(format_general_db_error(f"Adding Activity - 501: {current_user.name}", has_error[1]))
    except Exception as e:
      print()
      send_notification(format_general_db_error(f"Addidng Activity For => 501 Error:", e))
    send_notification(format_general_db_error(f"System 501 Error:", error))

    return render_template('errors/errors.html', title="501", system_error=error), 501