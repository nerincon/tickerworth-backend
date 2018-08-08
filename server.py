import os
import tornado.ioloop
import tornado.web
import tornado.log

import json
import requests


class MainHandler(tornado.web.RequestHandler):
  def get (self):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    print('getting something')
    r = requests.get('https://api.iextrading.com/1.0/stock/aapl/financials')
    tempdata = r.json()
    self.write(tempdata)


def make_app():
  return tornado.web.Application([(r"/api", MainHandler)])


if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '5000')))
  print('listening')
  tornado.ioloop.IOLoop.current().start()