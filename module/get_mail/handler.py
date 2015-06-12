from _config import IMAP_SSL
from config import IMAP_USERNAME, IMAP_PASSWORD
from config import POP3_USERNAME, POP3_PASSWORD
from module.get_mail.imap_client import SimpleImap
from module.get_mail.pop3_client import SimplePop3

__author__ = 'arnab'

import tornado
from module.send_mail.smtp_client import Email, SimpleMail
from module.send_mail.smtp_client import SmtpQueMail


class IMAPRequestHandler(tornado.web.RequestHandler):

    def get(self):
        i = SimpleImap(IMAP_USERNAME, IMAP_PASSWORD, IMAP_SSL)
        i.get_mail()
        self.render("templates/index.html")

    def post(self):
        self.render("templates/index.html")
