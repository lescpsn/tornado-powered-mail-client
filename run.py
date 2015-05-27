import tornado.ioloop
import tornado.web
# from smtp_module.send_mail import EmailHandler
from config import HOST, USERNAME, PASSWORD
from module.smtp.smtp_client import EmailHandler
from module.smtp.utils import QueMail


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/email/", EmailHandler)
])

if __name__ == "__main__":
    qm = QueMail.get_instance()
    qm.init(HOST, USERNAME, PASSWORD)
    qm.start()
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()