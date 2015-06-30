import tornado
from module.send_mail.smtp_client import Email, SimpleMail
from module.send_mail.smtp_client import SmtpQueMail
import email_config


class SMTPRequestHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/index.html")

    def post(self):
        qm = SmtpQueMail.get_instance()
        qm.send(Email(subject=self.get_argument('subject'), text=self.get_argument('message'),
                      adr_to=self.get_argument('email'), adr_from=email_config.SMTP_SENDER))
        self.render("templates/index.html")