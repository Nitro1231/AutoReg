import smtplib

# Set up the SMTP server and login credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587
email = ''
password = ''

# Set up the email message
from_addr = ''
to_addr = '' # Replace with the recipient's gateway address
subject = 'Test SMS'
body = 'This is a test SMS sent from Python.'

msg = f'Subject: {subject}\n\n{body}'

# Connect to the SMTP server and send the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email, password)
    server.sendmail(from_addr, to_addr, msg)
    print('SMS sent!')
except Exception as e:
    print('Error:', e)
finally:
    server.quit()