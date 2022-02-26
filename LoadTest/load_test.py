from tornado import httpclient, gen


class LoadTest:
    @gen.coroutine
    def load_test(self, concurrent):
        """self parameter is forwarded by the web socket handler"""
        """Load test: Fetches the urls and handles/processes the response as a message by the web socket handler"""

        http_client = httpclient.AsyncHTTPClient()
        urls=[]
        concurrent = int(concurrent)
        for i in range(concurrent):
            urls.append("http://localhost:8888/users/{:04d}".format(i))
        #futures = [http_client.fetch(url) for url in urls]
        #response = await asyncio.gather(*futures)
        waiter = gen.WaitIterator(*[http_client.fetch(url) for url in urls])

        while not waiter.done():
            try:
                response = yield waiter.next()
            except Exception as e:
                self.write_message(response.body)
                self.write_message("<br>")
                continue

            self.write_message(response.body)
            self.write_message("<br>")
