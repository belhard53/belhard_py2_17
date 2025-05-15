from celery import Celery
import smtplib

app = Celery('notifications', broker='pyamqp://guest@localhost//')

@app.task
def send_email(recipient, subject, body):
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login("your_email@example.com", "your_password")
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail("your_email@example.com", recipient, message)
    server.quit()

# пример использования
send_email.delay("user@example.com", "Welcome!", "Thank you for registering with us.")