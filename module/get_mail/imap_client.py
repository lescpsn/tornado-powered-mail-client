from datetime import datetime

__author__ = 'arnab'
from queue import Queue
from time import sleep
import time
from threading import Thread
from config import IMAP_USERNAME, IMAP_PASSWORD, IMAP_SSL, IMAP_OUTPUT_TEXT
import logging

log = logging.getLogger("ImapQueMail")


class SimpleImap:
    def __init__(self, username, password, imap_SSL):
        self.username = username
        self.password = password
        self.imap_SSL = imap_SSL

    def get_mail(self):
        import imaplib

        try:
            imap_conn = imaplib.IMAP4_SSL(self.imap_SSL)
            imap_conn.login(self.username, self.password)
            imap_conn.select('inbox')
            result, data = imap_conn.search(None, "UNSEEN")
            for num in data[0].split():
                typ, data = imap_conn.fetch(num, '(UID BODY[TEXT])')
                f = open(IMAP_OUTPUT_TEXT, "w")
                f.write('\n\nDate:%s\nMessage %s\n%s\n' % (datetime.now().strftime('%d-%m-%y %H:%M:%S'),num, data[0][1]))
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
        self.check_interval = 5

    def end(self):
        '''
        Waits until all emails will be sent and after that stops thread
        '''
        log.info("Stopping ImapQueMail thread...")
        self._do_quit = True
        self.join()
        log.info("Stopped.")

    def run(self):
        while not self._do_quit:
            if not self._queue.empty():
                log.debug(u"Connecting to Imap server: %s" % (IMAP_SSL))
                try:
                    while not self._queue.empty():
                        t = time.time()
                        eml = self._queue.get()
                        log.info(u"Receiving (qs=%i): %s" % (self._queue.qsize(), eml))
                        try:
                            self.imap_obj.get_mail()
                            log.warning(u"Sent (qs=%i,t=%f): %s" % (self._queue.qsize(), time.time() - t, eml))
                        except Exception as e:
                            log.error(u"Exception occured while getting email: %s" % eml)
                            log.exception(e)
                            self._queue.put(eml, False)
                            sleep(1)
                except Exception as e:
                    log.exception(e)

            sleep(self.check_interval)

    def get(self, eml):
        self._queue.put(eml, True, 5)
        log.debug(u'Accepted (qs=%i): %s' % (self._queue.qsize(), eml))

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = ImapQueMail()
        return cls.instance
