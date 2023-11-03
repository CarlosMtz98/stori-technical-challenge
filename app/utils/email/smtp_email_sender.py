import os
import smtplib, logging, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import definitions
from jinja2 import Environment, FileSystemLoader


class SmtpEmailSender:
    def __init__(self, host, port, sender_email, sender_password, logger):
        self.host = host
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.logger = logger if logger else logging.getLogger(__name__)
        self.context = ssl.create_default_context()
        self.server = None

    def load_template(self, template_file):
        app_root = definitions.ROOT_DIR
        file_path = os.path.join(app_root, "static/email_templates", template_file)
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
        except Exception as ex:
            self.logger.exception(ex)

    def connect(self):
        try:
            self.server = smtplib.SMTP_SSL(host=self.host, port=int(self.port), context=self.context)
            self.server.login(self.sender_email, self.sender_password)
        except Exception as ex:
            self.logger.exception(ex)

    def disconnect(self):
        if not self.server:
            self.logger.error("Cant disconnect server, there is no email server connection established")
            return

        self.server.quit()

    def render_template(self, template_file, params):
        try:
            html_template = self.load_template(template_file)
            template_loader = FileSystemLoader(searchpath='.')
            env = Environment(loader=template_loader)
            template = env.from_string(html_template)
            return template.render(params)

        except Exception as ex:
            self.logger.exception(ex)

    def send_email(self, recipient_email, subject, html_content):
        try:
            if not self.server:
                self.logger.error("No email server connection established")
                return

            email_content = MIMEText(html_content, "html")
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(email_content)
            self.server.sendmail(self.sender_email, recipient_email, msg.as_string())

        except Exception as ex:
            self.logger.exception(ex)
