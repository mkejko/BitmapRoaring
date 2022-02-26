import tornado.web
import tornado.ioloop
from datetime import date



class SessionRequestHandler(tornado.web.RequestHandler):
    def initialize(self, expensive_value):
        self.expensive_value = expensive_value
    def get(self):
        USERS = self.expensive_value
        curDate=date.today()
        long_unlogged_users=[]
        for i in range(len(USERS)):
            dayDif=curDate-USERS[i][2]
            if dayDif.days>7:
                long_unlogged_users.append(remove_prefix(str(USERS[i][1]), "BitMap")+"___"+str(USERS[i][2]))
            else:
                pass
        self.render("session.html", title="My title", number = len(long_unlogged_users), items=long_unlogged_users)


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]