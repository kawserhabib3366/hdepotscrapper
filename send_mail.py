import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_email_notification( body):

    sender_email="mikebatshon729@gmail.com"
    sender_password="asvm vihi emac nhih"
    receiver_email="mikebatshon@gmail.com"
    subject="Homedepot Bot Notifier"

    """
    Send an email notification using SMTP.
    
    Parameters:
    - sender_email: str, your email address
    - sender_password: str, your email password or app password
    - receiver_email: str, recipient's email address
    - subject: str, email subject
    - body: str, email body content
    """
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()





