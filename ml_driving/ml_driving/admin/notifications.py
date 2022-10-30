import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_notification(message):
  try:
      # return False  # TODO: DELETE THIS LINE
      key = os.environ.get('SENDGRID_API_KEY')
      sg = SendGridAPIClient(key)
      response = sg.send(message)
      if int(response.status_code) != 202:
        response = sg.send(Mail(
          from_email='dan.lucas2204@gmail.com',
          to_emails='dan.lucas2204@gmail.com',
          subject=f"MLDS Notification Error ",
          html_content=f"<h1>Notification returned with a status of {response.status_code}</h1>" \
                        f"<p>{message}</p>")
        )
      # return True
      return {'result': True, 'error': None}
  except Exception as e:
      # return False
      return {'result': False, 'error': e}

