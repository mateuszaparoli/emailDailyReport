#pip install schedule
#python send_daily_report.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule
import time

# Configuration
SMTP_SERVER = 'smtp.your-email-provider.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@example.com'
SENDER_PASSWORD = 'your-email-password'
RECIPIENT_EMAIL = 'recipient-email@example.com'
SUBJECT = 'Daily Report'

def create_email():
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = SUBJECT

    # Email body
    body = "This is the daily report. Please find the attached report."
    msg.attach(MIMEText(body, 'plain'))

    # File to be sent
    filename = "report.txt"
    attachment = open(filename, "rb")

    # Instance of MIMEBase and named as p
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")

    # Attach the instance 'part' to instance 'msg'
    msg.attach(part)

    # Close the attachment
    attachment.close()

    return msg

def send_email():
    try:
        msg = create_email()

        # Connect to the server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send the email
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Schedule the email to be sent daily at a specific time
schedule.every().day.at("08:00").do(send_email)

print("Scheduling complete. The script will now send emails daily at 08:00.")

while True:
    schedule.run_pending()
    time.sleep(60)

