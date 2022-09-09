import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def process_form(form):
  # email_to = "eruditebadger@gmail.com"
  # email_to = "dan2204.py@gmail.com"
  email_to = "dan.lucas2204@gmail.com"
  name = f"{form.first_name.data} {form.last_name.data}"
  subject_text = form.subject.data if form.subject.data else ">> Not Entered <<"
  body_head = '<h2><strong>Contact from ML Driving School</strong></h2>'
  body_name = f'<p><strong>Name: </strong> {name} </p>'
  body_email = f'<p><strong>Email: </strong> {form.email.data} </p>'
  body_phone = f'<p><strong>Phone: </strong> {form.phone.data} </p>'
  body_subject = f'<p><strong>Subject: </strong> {subject_text} </p>'
  body_message = f'<p><strong>Message: </strong> {form.details.data} </p>'
  body_footer = "<br/><p>This message is automated, please don't respond</p>"
  message = Mail(
    from_email='dan.lucas2204@gmail.com',
    to_emails=email_to,
    subject="Automated Message: You've recieved a message from MLDS",
    html_content=f"{body_head}\n{body_name}\n{body_email}\n{body_phone}\n" \
                  f"{body_subject}\n{body_message}\n{body_footer}")
  try:
      # return False  # TODO: DELETE THIS LINE
      key = os.environ.get('SENDGRID_API_KEY')
      sg = SendGridAPIClient(key)
      response = sg.send(message)
      if int(response.status_code) != 202:
        response = sg.send(Mail(
          from_email='dan.lucas2204@gmail.com',
          to_emails='dan.lucas2204@gmail.com',
          subject=f"MLDS Message Error ",
          html_content=f"<h1>Message returned with a status of {response.status_code}</h1>" \
                        f"<p>{name}</p><p>{body_message}</p>")
        )
      return True
  except Exception as e:
      return False
