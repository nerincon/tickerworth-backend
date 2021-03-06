import os
import tornado.ioloop
import tornado.web
import tornado.log
import psycopg2
from datetime import datetime, timedelta
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import numpy as np
import math
# problem with deploying matplotlib to heroku. Do not need right now, but if need it in heroku in the future go back to this url to solve problem. url: https://stackoverflow.com/questions/43697460/import-matplotlib-failing-on-heroku
#removed the matplotlib from requirements.txt. No need to modify Pipfile since Heroku is using requiremtns file I created.
# from matplotlib import style
# import matplotlib.pyplot as plt
# import matplotlib.mlab as mlab
from apifuncs import get_api_companies_list, get_api_dev, get_api_financials, get_api_financials_cache, get_api_stats, get_api_stats_cache, get_tr_chart_data, get_cr_chart_data, get_gp_chart_data, get_oe_chart_data, get_oi_chart_data, get_ni_chart_data, get_api_news, get_api_news_cache, get_api_main, get_api_main_cache, get_ca_chart_data, get_ta_chart_data, get_tl_chart_data, get_cc_chart_data, get_cd_chart_data, get_tc_chart_data, get_td_chart_data, get_se_chart_data, get_ogl_chart_data, get_cf_chart_data, get_api_ddm, get_api_ddm_cache

import json
import requests
import threading

# must put this (heroku config:set IS_HEROKU=True) in terminal in the app folder you are working on for the line after this to work. Without the parenthesis of course.
is_prod = os.environ.get('IS_HEROKU', None)


def companyListing():
  conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
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


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


if is_prod:
  print('In production. Timer has started for company listing check/update')
  set_interval(companyListing, 7200)
else:
  print('In Dev Mode. Timer not running')


def updateCompanyListing():
  print('Database updating. Data being loaded from API to get most current company listing.')
  conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
  cur = conn.cursor()
  cur.execute("DELETE FROM companylist")
  if is_prod:
    listings = get_api_companies_list()
  else:
    listings = get_api_dev()
  for company in listings:
    cur.execute("INSERT INTO companylist VALUES (DEFAULT,%s, %s, %s, %s, %s)",(company['symbol'], company['name'], company['date'], company['type'], company['iexId']))
    conn.commit()


companyListing()


class CompanyListingsHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    self.set_header('Content-Type', 'application/json')
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
    cur = conn.cursor()
    cur.execute("SELECT symbol, name  FROM companylist")
    company_list = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    company_list_json = json.dumps(company_list)
    self.write(company_list_json)
    cur.close()
    conn.close()


class CompanyMainHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    dt = datetime.utcnow()
    timeDelta = timedelta(minutes=1440)
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
    cur = conn.cursor()
    cur.execute("SELECT time_stamp FROM companymaininfo WHERE symbol = (%s) LIMIT 1", [ticker])
    row = cur.fetchone()
    if row != None:
      db_timestamp = row[0]
    if row == None:
      get_api_main(self, ticker)
    elif (dt - db_timestamp) < timeDelta:
      get_api_main_cache(self, ticker)
    else:
      get_api_main(self, ticker)



class monte_carlo(tornado.web.RequestHandler):
    def get(self, symbol):
      self.set_header("Access-Control-Allow-Origin", "*")
      self.set_header("Access-Control-Allow-Headers", "x-requested-with")
      self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
      self.set_header('Content-Type', 'application/json')
      #Dates
      start = datetime(2015, 1, 3)
      end = datetime(2017, 10, 4)
      
      prices = web.DataReader(symbol, 'iex',start, end)['close']
      returns = prices.pct_change()

      
      last_price = prices[-1]
      
      simulation_df = pd.DataFrame()
      num_simulations = 20
      predicted_days = 200

      #Create Each Simulation as a Column in df
      for x in range(num_simulations):
          count = 0
          daily_vol = returns.std()
          
          price_series = []
          
          #Append Start Value
          price = last_price * (1 + np.random.normal(0, daily_vol))
          price_series.append(price)
          
          #Series for Predicted Days
          for i in range(predicted_days):
              if count == 251:
                  break
              price = price_series[count] * (1 + np.random.normal(0, daily_vol))
              price_series.append(price)
              count += 1
      
          simulation_df[x] = price_series
      
      last_price = prices[-1]
      # fig = plt.figure()
      # style.use('bmh')
      
      # title = "Monte Carlo Simulation: " + str(predicted_days) + " Days"
      # plt.plot(simulation_df)
      # fig.suptitle(title,fontsize=18, fontweight='bold')
      # plt.xlabel('Day')
      # plt.ylabel('Price ($USD)')
      # plt.grid(True,color='grey')
      # plt.axhline(y=last_price, color='r', linestyle='-')
      # plt.savefig(symbol+".png")
      # plt.show()
      simulation_values_dict = simulation_df.to_dict('split')
      simulation_values_dict_modified = simulation_values_dict['data']
      simulation_values_dict_final = {}
      key = 0
      for line in simulation_values_dict_modified:
          key += 1
          simulation_values_dict_final[key] = line
      new_simulation_values_list = []
      for key, line in enumerate(simulation_values_dict_modified):
          new_simulation_values_list.append(dict([(key, line)]))
      final_simulation_values_send = json.dumps(new_simulation_values_list)
      self.write(final_simulation_values_send)



class CompanyKeyFinancialsHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    dt = datetime.utcnow()
    timeDelta = timedelta(minutes=1440)
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
    cur = conn.cursor()
    cur.execute("SELECT time_stamp FROM keyfinancials WHERE symbol = (%s) LIMIT 1", [ticker])
    row = cur.fetchone()
    if row != None:
      db_timestamp = row[0]
    if row == None:
      get_api_financials(self, ticker)
    elif (dt - db_timestamp) < timeDelta:
      get_api_financials_cache(self, ticker)
    else:
      get_api_financials(self, ticker)


class CompanyNewsHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    dt = datetime.utcnow()
    timeDelta = timedelta(minutes=1440)
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
    cur = conn.cursor()
    cur.execute("SELECT time_stamp FROM companynews WHERE symbol = (%s) LIMIT 1", [ticker])
    row = cur.fetchone()
    if row != None:
      db_timestamp = row[0]
    if row == None:
      get_api_news(self, ticker)
    elif (dt - db_timestamp) < timeDelta:
      get_api_news_cache(self, ticker)
    else:
      get_api_news(self, ticker)



class CompanyKeyStatsHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    dt = datetime.utcnow()
    timeDelta = timedelta(minutes=1440)
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
    cur = conn.cursor()
    cur.execute("SELECT time_stamp FROM keystats WHERE symbol = (%s) LIMIT 1", [ticker])
    row = cur.fetchone()
    if row != None:
      db_timestamp = row[0]
    if row == None:
      get_api_stats(self, ticker)
    elif (dt - db_timestamp) < timeDelta:
      get_api_stats_cache(self, ticker)
    else:
      get_api_stats(self, ticker)


class CompanyNameHandler(tornado.web.RequestHandler):
  def get(self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    print('getting company name')
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
    cur = conn.cursor()
    cur.execute("SELECT name FROM companylist WHERE symbol = (%s)", [ticker])
    company_name = cur.fetchone()
    company_name_dict = {'compname': x for x in company_name}
    self.write(company_name_dict)
    cur.close()
    conn.close()

class CompanyLogoHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    print('getting image')
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
    cur = conn.cursor()
    cur.execute("SELECT symbol FROM companyimage WHERE symbol = (%s)", [ticker])
    in_db = cur.fetchone()
    if in_db:
      cur.execute("SELECT url FROM companyimage WHERE symbol = (%s)", [ticker])
      logo = cur.fetchone()
      logo_dict = {'url': x for x in logo}
      print('getting logo from DB')
      print('url from db (modified): ' , logo_dict)
      self.write(logo_dict)
      cur.close()
      conn.close()
    else:
      r = requests.get('https://api.iextrading.com/1.0/stock/'+ ticker + '/logo')
      logodata = r.json()
      cur.execute("INSERT INTO companyimage VALUES (DEFAULT,%s, %s)",(ticker, logodata['url']))
      conn.commit()
      cur.execute("SELECT url FROM companyimage WHERE symbol = (%s)", [ticker])
      logo = cur.fetchone()
      logo_dict = {'url': x for x in logo}
      print('inserting logo to DB and getting it back from DB')
      print('logodata from api: ' , logodata)
      print('url from db (modified): ' , logo_dict)
      self.write(logo_dict)
      cur.close()
      conn.close()


class CompanyPriceHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    print('getting price')
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
    cur = conn.cursor()
    cur.execute("SELECT symbol FROM companyprice WHERE symbol = (%s)", [ticker])
    in_db = cur.fetchone()
    if in_db:
      cur.execute("SELECT price FROM companyprice WHERE symbol = (%s)", [ticker])
      price = cur.fetchone()
      price_dict = {'price': x for x in price}
      self.write(price_dict)
      cur.close()
      conn.close()
    else:
      r = requests.get('https://api.iextrading.com/1.0/stock/'+ ticker + '/price')
      pricedata = r.json()
      cur.execute("INSERT INTO companyprice VALUES (DEFAULT,%s, %s)",(ticker, pricedata))
      conn.commit()
      cur.execute("SELECT price FROM companyprice WHERE symbol = (%s)", [ticker])
      price = cur.fetchone()
      price_dict = {'price': x for x in price}
      self.write(price_dict)
      cur.close()
      conn.close()


class ChartTRHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_tr_chart_data(self, ticker)


class ChartCRHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_cr_chart_data(self, ticker)


class ChartGPHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_gp_chart_data(self, ticker)


class ChartOEHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_oe_chart_data(self, ticker)


class ChartOIHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_oi_chart_data(self, ticker)


class ChartNIHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_ni_chart_data(self, ticker)

class ChartCAHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_ca_chart_data(self, ticker)

class ChartTAHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_ta_chart_data(self, ticker)

class ChartTLHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_tl_chart_data(self, ticker)

class ChartCCHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_cc_chart_data(self, ticker)

class ChartCDHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_cd_chart_data(self, ticker)

class ChartTCHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_tc_chart_data(self, ticker)

class ChartTDHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_td_chart_data(self, ticker)


class ChartSEHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_se_chart_data(self, ticker)


class ChartCFHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_cf_chart_data(self, ticker)

class ChartOGLHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    get_ogl_chart_data(self, ticker)


class CompanyDDMHandler(tornado.web.RequestHandler):
  def get (self, ticker):
    print("setting headers!!!")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    dt = datetime.utcnow()
    timeDelta = timedelta(minutes=1440)
    conn = psycopg2.connect(os.environ.get('DATABASE_URL', 'postgres://postgres@localhost:5432/tickerworth'))
    cur = conn.cursor()
    cur.execute("SELECT time_stamp FROM companyddm WHERE symbol = (%s) LIMIT 1", [ticker])
    row = cur.fetchone()
    if row != None:
      db_timestamp = row[0]
    if row == None:
      get_api_ddm(self, ticker)
    elif (dt - db_timestamp) < timeDelta:
      get_api_ddm_cache(self, ticker)
    else:
      cur.execute("DELETE FROM companyddm WHERE symbol = (%s)", [ticker])
      get_api_ddm(self, ticker)


def make_app():
  return tornado.web.Application([
    (r"/main/([^/]+)", CompanyMainHandler),
    (r"/listings", CompanyListingsHandler),
    (r"/mcarlo/([^/]+)", monte_carlo),
    (r"/fin/([^/]+)", CompanyKeyFinancialsHandler),
    (r"/ddm/([^/]+)", CompanyDDMHandler),
    (r"/news/([^/]+)", CompanyNewsHandler),
    (r"/logo/([^/]+)", CompanyLogoHandler),
    (r"/price/([^/]+)", CompanyPriceHandler),
    (r"/name/([^/]+)", CompanyNameHandler),
    (r"/stats/([^/]+)", CompanyKeyStatsHandler),
    (r"/trchart/([^/]+)", ChartTRHandler),
    (r"/crchart/([^/]+)", ChartCRHandler),
    (r"/gpchart/([^/]+)", ChartGPHandler),
    (r"/oechart/([^/]+)", ChartOEHandler),
    (r"/oichart/([^/]+)", ChartOIHandler),
    (r"/nichart/([^/]+)", ChartNIHandler),
    (r"/cachart/([^/]+)", ChartCAHandler),
    (r"/tachart/([^/]+)", ChartTAHandler),
    (r"/tlchart/([^/]+)", ChartTLHandler),
    (r"/ccchart/([^/]+)", ChartCCHandler),
    (r"/cdchart/([^/]+)", ChartCDHandler),
    (r"/tcchart/([^/]+)", ChartTCHandler),
    (r"/tdchart/([^/]+)", ChartTDHandler),
    (r"/sechart/([^/]+)", ChartSEHandler),
    (r"/cfchart/([^/]+)", ChartCFHandler),
    (r"/oglchart/([^/]+)", ChartOGLHandler)])


if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '5000')))
  print('listening')
  tornado.ioloop.IOLoop.current().start()