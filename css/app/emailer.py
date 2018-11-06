import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(recipient, subject, recipient_username, name):
    thread = threading.Thread(
        target=_threaded_send_email,
        args=(recipient, subject, recipient_username, name),
    )

    thread.daemon = True
    thread.start()


def _threaded_send_email(recipient, subject, recipient_username, name):
    username = 'cssurvivalwebsite@gmail.com'
    password = 'CSsurvivalPassword'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(username, password)
    except:
        print('Something went wrong')

    msg = MIMEMultipart()
    msg['Subject'] = "Thread Updated!"
    msg['From'] = username
    msg['To'] = recipient

    html = """
    <html>
      <head></head>
      <body>
        <p>Hello {recipient_username}.<br>
           The thread "{name}" has been updated.
        </p>
      </body>
    </html>
    """.format(**locals())

    email = MIMEText(html, 'html')
    msg.attach(email)

    server.sendmail(username, [recipient], msg.as_string())
    server.quit()
