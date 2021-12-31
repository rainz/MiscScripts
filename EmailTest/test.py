import os
import sys
import sl4a
import glob
import mimetypes 
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from getpass import getpass

droid = sl4a.Android()
#line = droid.dialogGetInput()
#droid.makeToast("toast")

def sendemail(email_name, email_user, email_pswd, mailto, subject, body, attachments):
  import smtplib

  # DON'T CHANGE THIS!
  # ...unless you're rewriting this script for your own SMTP server!
  smtp_server = 'smtp.gmail.com'
  #smtp_port = 587
  smtp_port = 465

  # Build an SMTP compatible message
  msg = MIMEMultipart()
  msg['Subject'] = subject
  msg['To'] = mailto
  msg['From'] = email_name + " <" + email_user + ">"
  msg.attach(MIMEText(body, 'plain'))
  #attach_files(msg, attachments)

  # Attempt to connect and send the email
  try:
    smtpObj = '' # Declare within this block.
    # Check for SMTP over SSL by port number and connect accordingly
    if( smtp_port == 465):
      smtpObj = smtplib.SMTP_SSL(smtp_server,smtp_port)
    else:
      smtpObj = smtplib.SMTP(smtp_server,smtp_port)
    smtpObj.ehlo()
    # StartTLS if using the default TLS port number
    if(smtp_port == 587):
      smtpObj.starttls()
      smtpObj.ehlo
    # Login, send and close the connection.
    smtpObj.login(email_user, email_pswd)
    smtpObj.sendmail(email_user, mailto, msg.as_string())
    smtpObj.close()
    return 1  # Return 1 to denote success!
  except (Exception) as ex:
    # Print error and return 0 on failure.
    print(ex)
    return 0

pswd = getpass()
#print(pswd)
sendemail("YY ZZ", "rainzforever", pswd, "rainzforever@hotmail.com", "From android", "Blah", None)
