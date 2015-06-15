import tornado.ioloop
import tornado.web
# from smtp_module.send_mail import EmailHandler
from email_config import SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD
from module.get_mail.handler import IMAPRequestHandler
from module.get_mail.imap_client import ImapQueMail
from module.send_mail.handler import SMTPRequestHandler
from module.send_mail.smtp_client import SmtpQueMail


application = tornado.web.Application([
    (r"/send_email/", SMTPRequestHandler),
    (r'/get_email/', IMAPRequestHandler)
])

if __name__ == "__main__":
    from log_config import *
    sqm = SmtpQueMail.get_instance()
    sqm.init(SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD)
    sqm.start()
    iqm = ImapQueMail.get_instance()
    iqm.init()
    iqm.start()
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()