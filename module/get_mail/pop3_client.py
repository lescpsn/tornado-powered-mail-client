__author__ = 'arnab'


class SimplePop3:
    def __init__(self, username, password, pop3_SSL):
        self.username = username
        self.password = password
        self.pop3_SSL

    def get_mail(self):
        import poplib
        from email import parser
        pop_conn = poplib.POP3_SSL('pop.gmail.com')
        pop_conn.user('myusername')
        pop_conn.pass_('mypassword')
        #Get messages from server:
        messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
        # Concat message pieces:
        messages = ["\n".join(mssg[1]) for mssg in messages]
        #Parse message intom an email object:
        messages = [parser.Parser().parsestr(mssg) for mssg in messages]
        for message in messages:
            print(message['subject'])
            print(message.get_payload())
        pop_conn.quit()