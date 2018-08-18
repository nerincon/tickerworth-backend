import os
import tornado.ioloop
import tornado.web
import tornado.log
import psycopg2
from datetime import datetime, timedelta
from apifuncs import get_api_companies_list, get_api_dev, get_api_financials, get_api_financials_cache, get_api_stats, get_api_stats_cache, get_tr_chart_data, get_cr_chart_data, get_gp_chart_data, get_oe_chart_data, get_oi_chart_data, get_ni_chart_data, get_api_news, get_api_news_cache


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




class CompanyKeyFinancialsHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    dt = datetime.utcnow()
    timeDelta = timedelta(minutes=1440)
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT time_stamp FROM keyfinancials WHERE symbol = (%s) LIMIT 1", [slug])
    row = cur.fetchone()
    if row != None:
      db_timestamp = row[0]
    if row == None:
      get_api_financials(self, slug)
    elif (dt - db_timestamp) < timeDelta:
      get_api_financials_cache(self, slug)
    else:
      get_api_financials(self, slug)


class CompanyNewsHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    dt = datetime.utcnow()
    timeDelta = timedelta(minutes=1440)
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT time_stamp FROM companynews WHERE symbol = (%s) LIMIT 1", [slug])
    row = cur.fetchone()
    if row != None:
      db_timestamp = row[0]
    if row == None:
      get_api_news(self, slug)
    elif (dt - db_timestamp) < timeDelta:
      get_api_news_cache(self, slug)
    else:
      get_api_news(self, slug)

class CompanyKeyStatsHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    dt = datetime.utcnow()
    timeDelta = timedelta(minutes=1440)
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT time_stamp FROM keystats WHERE symbol = (%s) LIMIT 1", [slug])
    row = cur.fetchone()
    if row != None:
      db_timestamp = row[0]
    if row == None:
      get_api_stats(self, slug)
    elif (dt - db_timestamp) < timeDelta:
      get_api_stats_cache(self, slug)
    else:
      get_api_stats(self, slug)


class CompanyNameHandler(tornado.web.RequestHandler):
  def get(self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    print('getting company name')
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT name FROM companylist WHERE symbol = (%s)", [slug])
    company_name = cur.fetchone()
    company_name_dict = {'compname': x for x in company_name}
    self.write(company_name_dict)
    cur.close()
    conn.close()

class CompanyLogoHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    print('getting image')
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT symbol FROM companyimage WHERE symbol = (%s)", [slug])
    in_db = cur.fetchone()
    if in_db:
      cur.execute("SELECT url FROM companyimage WHERE symbol = (%s)", [slug])
      logo = cur.fetchone()
      logo_dict = {'url': x for x in logo}
      print('getting logo from DB')
      print('url from db (modified): ' , logo_dict)
      self.write(logo_dict)
      cur.close()
      conn.close()
    else:
      r = requests.get('https://api.iextrading.com/1.0/stock/'+ slug + '/logo')
      logodata = r.json()
      cur.execute("INSERT INTO companyimage VALUES (DEFAULT,%s, %s)",(slug, logodata['url']))
      conn.commit()
      cur.execute("SELECT url FROM companyimage WHERE symbol = (%s)", [slug])
      logo = cur.fetchone()
      logo_dict = {'url': x for x in logo}
      print('inserting logo to DB and getting it back from DB')
      print('logodata from api: ' , logodata)
      print('url from db (modified): ' , logo_dict)
      self.write(logo_dict)
      cur.close()
      conn.close()


class ChartTRHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_tr_chart_data(self, slug)


class ChartCRHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_cr_chart_data(self, slug)


class ChartGPHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_gp_chart_data(self, slug)


class ChartOEHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_oe_chart_data(self, slug)


class ChartOIHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_oi_chart_data(self, slug)


class ChartNIHandler(tornado.web.RequestHandler):
  def get (self, slug):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_ni_chart_data(self, slug)


def make_app():
  return tornado.web.Application([
    (r"/fin/([^/]+)", CompanyKeyFinancialsHandler),
    (r"/news/([^/]+)", CompanyNewsHandler),
    (r"/logo/([^/]+)", CompanyLogoHandler),
    (r"/name/([^/]+)", CompanyNameHandler),
    (r"/stats/([^/]+)", CompanyKeyStatsHandler),
    (r"/trchart/([^/]+)", ChartTRHandler),
    (r"/crchart/([^/]+)", ChartCRHandler),
    (r"/gpchart/([^/]+)", ChartGPHandler),
    (r"/oechart/([^/]+)", ChartOEHandler),
    (r"/oichart/([^/]+)", ChartOIHandler),
    (r"/nichart/([^/]+)", ChartNIHandler)])


if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '5000')))
  print('listening')
  tornado.ioloop.IOLoop.current().start()