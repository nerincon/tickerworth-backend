import os
import tornado.ioloop
import tornado.web
import tornado.log
import psycopg2
from datetime import datetime
from apifuncs import get_api_companies_list, get_api_dev


import json
import requests
import threading


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

env = os.environ.get("PYTHON_ENV")
if env == "production":
  print('In production. Timer has started for company listing check/update')
  set_interval(companyListing, 7200)
else:
  print('In Dev Mode. Timer not running')


def updateCompanyListing():
  env = os.environ.get("PYTHON_ENV")
  print('Database updating. Data being loaded from API to get most current company listing.')
  conn = psycopg2.connect("dbname=tickerworth user=postgres")
  cur = conn.cursor()
  cur.execute("DELETE FROM companylist")
  if env == "production":
    listings = get_api_companies_list()
  else:
    listings = get_api_dev()
  for company in listings:
    cur.execute("INSERT INTO companylist VALUES (DEFAULT,%s, %s, %s, %s, %s)",(company['symbol'], company['name'], company['date'], company['type'], company['iexId']))
    conn.commit()

def companyListing():
  conn = psycopg2.connect("dbname=tickerworth user=postgres")
  cur = conn.cursor()
  cur.execute("SELECT EXTRACT(YEAR FROM pulldate) as year, EXTRACT(MONTH FROM pulldate) as month, EXTRACT(DAY FROM pulldate) as day FROM companylist LIMIT 1")
  pulldate = cur.fetchone()
  if pulldate == None:
    updateCompanyListing()
    cur.close()
    conn.close()
  else:
    db_date = []
    for d in pulldate:
      db_date.append(int(d))
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    currentDay = datetime.now().day
    if db_date[0] == currentYear and db_date[1] == currentMonth and db_date[2] == currentDay:
      print('Database has most current data')
    else:
      updateCompanyListing()
      cur.close()
      conn.close()


companyListing()

class MainHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    print('getting something')
    # symbol = self.get_query_argument('symbol', None)
    r = requests.get('https://api.iextrading.com/1.0/stock/'+ slug + '/financials?period=annual')
    tempdata = r.json()
    # print(tempdata['symbol'])
    self.write(tempdata)


def make_app():
  return tornado.web.Application([(r"/fin/([^/]+)", MainHandler)])


if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '5000')))
  print('listening')
  tornado.ioloop.IOLoop.current().start()