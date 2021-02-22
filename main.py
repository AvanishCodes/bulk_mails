import email, smtplib, ssl, csv

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 465  # For SSL
user_email = input("Enter your email and hit enter: ")
password = input("Type your password and press enter: ")
# 

# Create a secure SSL context
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL(user_email, port, context=context) as server:
    # server.login(user_email, password)
with open("contacts_file.csv") as file:
    reader = csv.reader(file)
    # next(reader)  # Skip header row
    for name, receiver_email in reader:
        print(f"{name}, {receiver_email}")
        subject = "Test Email"
        message = MIMEMultipart()
        message["From"] = user_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails
        body = f"""Hi {name}
        
        Ruminate thanks you for attending the webinar by Mr. Pranjal kamra on February 21st, 2021.
        
        Here is your certificate."""
        message.attach(MIMEText(body, "plain"))
        filename = f"{receiver_email}.pdf".strip()  # In same directory as script
        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        message.attach(part)
        text = message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(user_email, password)
            server.sendmail(user_email, receiver_email, text)
        # body = "This is an email with attachment sent from Python"
        # receiver_email = "your@gmail.com"
        # server.sendmail(
        #     user_email,
        #     receiver_email,
        #     message.format(name=name),
        # )
        print(f"email sent to {receiver_email}")