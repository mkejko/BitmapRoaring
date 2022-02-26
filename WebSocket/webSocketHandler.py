import tornado.websocket
from LoadTest.load_test import LoadTest


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print("New connection")      
        self.write_message("Connection opened! ")
        self.write_message("<br>")

    def on_message(self, message):
        print("Number of concurrent sessions {}".format(message))

        if message.isdigit():
            LoadTest.load_test(self, message)

    def on_close(self, message):
        print("Connection closed")