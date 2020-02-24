# Import smtplib for the actual sending function
import smtplib
import getpass

# Import the email modules we'll need
from email.mime.text import MIMEText

passwd = getpass.getpass()

msg = MIMEText("Msg body")

me = "rainzforever@hotmail.com"
you = "yuzhao30@yahoo.com"
msg['Subject'] = 'From raspberry pi'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('smtp.live.com', 587)
s.set_debuglevel(1)
s.ehlo()
s.starttls() 
s.ehlo()
s.login(me, passwd)
s.sendmail(me, [you], msg.as_string())
s.quit()