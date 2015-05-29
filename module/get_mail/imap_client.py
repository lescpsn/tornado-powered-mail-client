__author__ = 'arnab'


class SimpleImap:
    def __init__(self, username, password, imap_SSL):
        self.username = username
        self.password = password
        self.imap_SSL = imap_SSL

    def get_mail(self):
        import imaplib
        from email.parser import Parser
        imap_conn = imaplib.IMAP4_SSL(self.imap_SSL)
        imap_conn.login(self.username, self.password)
        imap_conn.select('inbox')
        result, data = imap_conn.search(None, "UNSEEN")
        for num in data[0].split():
            typ, data  = imap_conn.fetch(num, '(UID BODY[TEXT])')
            # = imap_conn.fetch(num, '(RFC822)')
            print('Message %s\n%s\n' % (num, data[0][1]))

        imap_conn.close()
        imap_conn.logout()