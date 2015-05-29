from config import POP3_USERNAME, POP3_PASSWORD
from module.get_mail.utils import SimplePop3

__author__ = 'arnab'

import tornado
from module.send_mail.utils import Email, SimpleMail
from module.send_mail.utils import QueMail


class POP3RequestHandler(tornado.web.RequestHandler):

    def get(self):
        s = SimplePop3(username=POP3_USERNAME, password=POP3_PASSWORD, pop3_SSL='')
        self.render("templates/index.html")

    def post(self):

        self.render("templates/index.html")