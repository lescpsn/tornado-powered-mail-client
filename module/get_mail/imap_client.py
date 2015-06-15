from datetime import datetime

__author__ = 'arnab'
from queue import Queue
from time import sleep
from threading import Thread
from email_config import IMAP_USERNAME, IMAP_PASSWORD, IMAP_SSL, IMAP_OUTPUT_TEXT
import email
import logging
from bs4 import BeautifulSoup

log = logging.getLogger("ImapQueMail")


class SimpleImap:
    def __init__(self, username, password, imap_SSL):
        self.username = username
        self.password = password
        self.imap_SSL = imap_SSL
        self.raw_email = None

    def get_email_body(self):
        b = email.message_from_string(self.raw_email)
        if b.is_multipart():
            for payload in b.get_payload():
                return payload.get_payload()
        else:
            return b.get_payload()

    def purify_message(self):
        soap = BeautifulSoup(self.get_email_body())
        return soap.prettify()

    def get_mail(self):
        import imaplib

        try:
            imap_conn = imaplib.IMAP4_SSL(self.imap_SSL)
            imap_conn.login(self.username, self.password)
            imap_conn.select('inbox')
            result, data = imap_conn.search(None, "UNSEEN")
            for num in data[0].split():
                n, ndata = imap_conn.fetch(num, "(RFC822)")
                self.raw_email = '%s' % ndata[0][1]
                msg = self.raw_email
                f = open(IMAP_OUTPUT_TEXT, "r+")
                old = f.read()
                f.seek(0)
                f.write(old + '\n\nDate:%s\nMessage %s\n%s\n' % (datetime.now().strftime('%d-%m-%y %H:%M:%S'), num,
                                                                 msg))
                f.flush()
            imap_conn.close()
            imap_conn.logout()

        except Exception as e:
            raise e


class ImapQueMail(Thread):
    instance = None

    def init(self, queue_size=100):
        self._queue = Queue(queue_size)
        log.info(
            "Initializing ImapQueMail with queue size %i. Using IMAP server: %s." % (queue_size, IMAP_SSL))
        self.imap_obj = SimpleImap(IMAP_USERNAME, IMAP_PASSWORD, IMAP_SSL)

    def __init__(self):
        Thread.__init__(self)
        self._do_quit = False
        self.setName("ImapQueMail")
        self.imap_obj = None
        self.check_interval = 30

    def run(self):

        while True:
            log.debug(u"Connecting to Imap server: %s" % (IMAP_SSL))
            try:

                self.imap_obj.get_mail()
                log.debug(u"Got mail from Imap server: %s" % (IMAP_SSL))

            except Exception as e:
                log.error(u"Exception occurred while getting email")
                log.exception(e)
                sleep(1)
            sleep(self.check_interval)

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = ImapQueMail()
        return cls.instance
