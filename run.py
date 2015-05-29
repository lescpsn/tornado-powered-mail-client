import tornado.ioloop
import tornado.web
# from smtp_module.send_mail import EmailHandler
from config import SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD
from module.get_mail.handler import IMAPRequestHandler
from module.send_mail.handler import SMTPRequestHandler
from module.send_mail.smtp_client import QueMail


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/email/", SMTPRequestHandler),
    (r'/get_email/', IMAPRequestHandler)
])

if __name__ == "__main__":
    qm = QueMail.get_instance()
    qm.init(SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD)
    qm.start()
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()