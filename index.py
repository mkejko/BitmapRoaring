import asyncio
import json
import Data.generateTestUsers as users 
import tornado.web
import tornado.ioloop
import tornado.websocket
from tornado import httpclient, gen
from tornado.gen import multi
from datetime import date
from WebSocket.webSocketHandler import WebSocketHandler
from sessionRequestHandler import SessionRequestHandler



class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class tagRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("tag.html")

class loadTestRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("LoadTest/load_test.html")


class tagsRequestHandler(tornado.web.RequestHandler):
    def get(self,tag):
        tag=int(tag)
        tagsList=users.generate_User_stats(users.read_users_from_file("testUsers.txt"))
        usersList=users.check_uid_for_tag(users.read_users_from_file("testUsers.txt"), tag)
        for i in range(len(tagsList)):
            tagsList[i][0]="<a href='/tags/{}'>".format(i+1)+tagsList[i][0]+"</a>"
        if tag==0:
            self.write(json.dumps(tagsList))
        elif tag<=10:
            for i in range(len(usersList)):
                usersList[i]="<a href='/users/"+str(usersList[i]).removeprefix("user")+"'>"+usersList[i]+"</a>"
            self.write(json.dumps(usersList))
        else:
            self.write("")

class tagAmountRequestHandler(tornado.web.RequestHandler):
    def get(self,tag):
        tag=int(tag)
        tagsList=users.generate_User_stats(users.read_users_from_file("testUsers.txt"))
        amount=users.get_amount_for_tag(users.read_users_from_file("testUsers.txt"), tag)
        self.write(json.dumps(amount))


class userRequestHandler(tornado.web.RequestHandler):
    async def get(self,usr):
        usr=int(usr)
        usrs= users.read_users_from_file()
        if usr>len(usrs):
            self.write("No user")
            return
        for i in range(len(usrs)):
            usrs[i][1]=usrs[i][1].to_array().tolist()     
        self.set_status(200)
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(usrs[usr][1]))


if __name__ == "__main__":
    import random
    USERS = users.read_users_from_file()
    for i in range(len(USERS)):
        USERS[i].append(date(2022,random.randint(1,2),random.randint(1,date.today().day)))
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/tag", tagRequestHandler),
        (r"/session", SessionRequestHandler, {'expensive_value': USERS}),
        (r"/tags/([0-9]{1,2})", tagsRequestHandler),
        (r"/tag_amount/([0-9]{1,2})", tagAmountRequestHandler),
        (r"/users/([0-9]{4})", userRequestHandler),
        (r"/ws/", WebSocketHandler),
        (r"/load_test/", loadTestRequestHandler)
    ])

    port = 8888
    http_client = httpclient.HTTPClient()
    
    app.listen(port)
    print(f"Listening on port {port}")
    tornado.ioloop.IOLoop.current().start()
