from sendgrid.helpers.mail import Mail, To


def format_contact_form(form):
  email_to_1 = "dan2204.py@gmail.com"
  email_to_2 = "eruditebadger@gmail.com"
  email_to_3 = "heidilouwho@googlemail.com"
  
  name = f"{form.first_name.data} {form.last_name.data}"
  subject_text = form.subject.data if form.subject.data else ">> Not Entered <<"
  
  body_head = '<h2><strong>Contact from ML Driving School</strong></h2>'
  body_name = f'<p><strong>Name: </strong> {name} </p>'
  body_email = f'<p><strong>Email: </strong> {form.email.data} </p>'
  body_phone = f'<p><strong>Phone: </strong> {form.phone.data} </p>'
  body_subject = f'<p><strong>Subject: </strong> {subject_text} </p>'
  body_message = f'<p><strong>Message: </strong> {form.details.data} </p>'
  body_auth = f'<br/><p><a href="https://dan2204py.eu.pythonanywhere.com/admin/contacts" style="color: #ff0000">Log in to admin to view contact</a></p>'
  body_footer = "<br/><p>This message is automated, please don't respond</p>"
  
  return Mail(
    from_email='dan.lucas2204@gmail.com',
    to_emails=email_to_1,
    # to_emails=[To(email_to_1), To(email_to_2), To(email_to_3)],
    is_multiple=True,
    subject="Automated Message: You've recieved a Contact Message from MLDS",
    html_content=f"{body_head}\n{body_name}\n{body_email}\n{body_phone}\n" \
                  f"{body_subject}\n{body_message}\n{body_auth}\n\n{body_footer}")
  
  
def format_review_form(form):
  email_to_1 = "dan2204.py@gmail.com"
  email_to_2 = "eruditebadger@gmail.com"
  email_to_3 = "heidilouwho@googlemail.com"
  
  body_head = '<h2><strong>Review from ML Driving School</strong></h2>'
  body_name = f'<p><strong>Name: </strong> {form.name.data} </p>'
  body_email = f'<p><strong>Email: </strong> {form.email.data} </p>'
  body_message = f'<p><strong>Review: </strong> {form.details.data} </p>'
  body_auth = f'<br/><p><a href="https://dan2204py.eu.pythonanywhere.com/admin/reviews" style="color: #ff0000">Log in to Admin to approve</a></p>'
  body_footer = "<br/><p>This message is automated, please don't respond</p>"
  
  return Mail(
    from_email='dan.lucas2204@gmail.com',
    to_emails=email_to_1,
    # to_emails=[To(email_to_1), To(email_to_2), To(email_to_3)],
    is_multiple=True,
    subject=F"Automated Message: You've recieved a Review from {form.email.data}",
    html_content=f"{body_head}\n{body_name}\n{body_email}\n{body_message}\n" \
                  f"{body_auth}\n\n{body_footer}")
  
  
def format_error_form(form, e):
  # email_to = "dan.lucas2204@gmail.com"
  email_to_1 = "dan2204.py@gmail.com"
  email_to_2 = "eruditebadger@gmail.com"
  email_to_3 = "heidilouwho@googlemail.com"
  
  message = ""
  for item in form:
    if item.data == 5 and type(item.data) == int:
      break
    message += f"<p><strong>{item.name}:</strong> {item.data}</p><br/>"
  message += f"<p><strong>Error:</strong> <br/>{e}</p>"
  return Mail(
    from_email='dan.lucas2204@gmail.com',
    to_emails=email_to_1,
    subject=F"Automated Message: Website DB Error - MLDS",
    html_content=message)
  

def format_general_db_error(area, e):
  email_to_1 = "dan2204.py@gmail.com"
  email_to_2 = "eruditebadger@gmail.com"
  email_to_3 = "heidilouwho@googlemail.com"
  # email_to = "dan.lucas2204@gmail.com"
  
  message = ""  
  message += f"<p><strong>Area: </strong>{ area }</p><br/>"
  message += f'<p><strong>Error Message: </strong><br/>{ e }</p>'
  return Mail(
    from_email='dan.lucas2204@gmail.com',
    to_emails=email_to_1,
    subject=F"Automated Message: Website DB Error - MLDS",
    html_content=message)