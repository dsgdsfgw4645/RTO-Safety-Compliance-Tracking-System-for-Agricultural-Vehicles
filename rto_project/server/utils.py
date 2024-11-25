import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import firebase_admin
from firebase_admin import messaging
import requests
import logging
from datetime import datetime

class NotificationManager:
    def __init__(self):
        # Email configuration
        self.email_sender = "your-email@gmail.com"
        self.email_password = "your-app-password"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        # Initialize Firebase
        try:
            firebase_admin.initialize_app()
        except ValueError:
            pass  # App already initialized

        # Setup logging
        logging.basicConfig(
            filename='logs/notifications.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def send_email(self, recipient, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_sender, self.email_password)
            server.send_message(msg)
            server.quit()

            logging.info(f"Email sent to {recipient}")
            return True
        except Exception as e:
            logging.error(f"Email sending failed: {str(e)}")
            return False

    def send_mobile_notification(self, token, title, body):
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=token
            )
            response = messaging.send(message)
            logging.info(f"Mobile notification sent: {response}")
            return True
        except Exception as e:
            logging.error(f"Mobile notification failed: {str(e)}")
            return False

    def send_violation_alert(self, plate_number, location, image_path):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"""
        Safety Violation Detected
        License Plate: {plate_number}
        Location: {location}
        Time: {timestamp}
        """

        # Send email to authorities
        self.send_email(
            "authority@example.com",
            "Safety Violation Alert",
            message
        )

        # Send mobile notification
        self.send_mobile_notification(
            "authority-device-token",
            "Safety Violation",
            f"Vehicle {plate_number} detected without safety markers"
        )

def log_event(event_type, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{timestamp} - {event_type}: {details}")