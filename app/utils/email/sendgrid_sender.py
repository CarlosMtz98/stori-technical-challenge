import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content


class SendgridSender:
    def __init__(self, api_key, from_email):
        self.key = api_key
        self.sg = sendgrid.SendGridAPIClient(api_key=self.key)
        self.from_email = from_email

    def send_email(self, to_email, subject, data):
        content = Content("text/plain", "Hello World")
        mail = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=content)
        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        return self.sg.client.mail.send.post(request_body=mail_json)