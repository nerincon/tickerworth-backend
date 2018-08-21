import requests
import json
import psycopg2
from pprint import pprint
from datetime import datetime


def get_api_dev():
    with open('companies_dev.json') as json_data:
        company_list_dev = json.load(json_data)
        json_data.close()
        # pprint(d)
        return company_list_dev


def get_api_companies_list():
    r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
    companies_list = r.json()
    return companies_list


def get_tr_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, totalrevenue as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    tr_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    tr_data_json = json.dumps(tr_data)
    self.write(tr_data_json)
    cur.close()
    conn.close()


def get_cr_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, costofrevenue as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    cr_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cr_data_json = json.dumps(cr_data)
    self.write(cr_data_json)
    cur.close()
    conn.close()


def get_gp_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, grossprofit as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    gp_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    gp_data_json = json.dumps(gp_data)
    self.write(gp_data_json)
    cur.close()
    conn.close()


def get_oe_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, operatingexpense as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    oe_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    oe_data_json = json.dumps(oe_data)
    self.write(oe_data_json)
    cur.close()
    conn.close()


def get_oi_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, operatingincome as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    oi_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    oi_data_json = json.dumps(oi_data)
    self.write(oi_data_json)
    cur.close()
    conn.close()


def get_ni_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, netincome as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    ni_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    ni_data_json = json.dumps(ni_data)
    self.write(ni_data_json)
    cur.close()
    conn.close()


def get_ca_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, currentassets as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    ca_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    ca_data_json = json.dumps(ca_data)
    self.write(ca_data_json)
    cur.close()
    conn.close()

def get_ta_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, totalassets as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    ta_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    ta_data_json = json.dumps(ta_data)
    self.write(ta_data_json)
    cur.close()
    conn.close()

def get_tl_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, totalliabilities as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    tl_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    tl_data_json = json.dumps(tl_data)
    self.write(tl_data_json)
    cur.close()
    conn.close()

def get_cc_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, currentcash as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    cc_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cc_data_json = json.dumps(cc_data)
    self.write(cc_data_json)
    cur.close()
    conn.close()

def get_cd_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, currentdebt as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    cd_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cd_data_json = json.dumps(cd_data)
    self.write(cd_data_json)
    cur.close()
    conn.close()

def get_tc_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, totalcash as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    tc_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    tc_data_json = json.dumps(tc_data)
    self.write(tc_data_json)
    cur.close()
    conn.close()

def get_td_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, totaldebt as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    td_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    td_data_json = json.dumps(td_data)
    self.write(td_data_json)
    cur.close()
    conn.close()

def get_se_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, shareholderequity as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    se_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    se_data_json = json.dumps(se_data)
    self.write(se_data_json)
    cur.close()
    conn.close()

def get_cf_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, cashflow as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    cf_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cf_data_json = json.dumps(cf_data)
    self.write(cf_data_json)
    cur.close()
    conn.close()

def get_ogl_chart_data(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, operatinggainsandloses as y FROM keyfinancials  WHERE symbol = (%s)", [slug])
    ogl_data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    ogl_data_json = json.dumps(ogl_data)
    self.write(ogl_data_json)
    cur.close()
    conn.close()


def get_api_financials(self, slug):
    print('requesting API for key financials')
    r = requests.get('https://api.iextrading.com/1.0/stock/'+ slug + '/financials?period=annual')
    findata = r.json()
    dt = datetime.utcnow()
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM keyfinancials WHERE symbol = (%s)", [slug])
    for report in findata['financials']:
        cur.execute("""INSERT INTO keyfinancials VALUES (DEFAULT,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (slug, dt, report['reportDate'], report['grossProfit'], report['costOfRevenue'], report['operatingRevenue'], report['totalRevenue'], 
        report['operatingIncome'], report['netIncome'], report['researchAndDevelopment'], report['operatingExpense'], report['currentAssets'],
        report['totalAssets'], report['totalLiabilities'], report['currentCash'], report['currentDebt'], report['totalCash'], report['totalDebt'],
        report['shareholderEquity'], report['cashChange'], report['cashFlow'], report['operatingGainsLosses']))
        conn.commit()
    cur.execute("""SELECT to_char(reportdate, 'YYYY:MM:DD') as reportdate, grossprofit::float8::numeric::money, costofrevenue::float8::numeric::money, 
    operatingrevenue::float8::numeric::money, totalrevenue::float8::numeric::money, operatingincome::float8::numeric::money, netincome::float8::numeric::money,
    researchanddevelopment::float8::numeric::money, operatingexpense::float8::numeric::money, currentassets::float8::numeric::money, totalassets::float8::numeric::money,
    totalliabilities::float8::numeric::money, currentcash::float8::numeric::money, currentdebt::float8::numeric::money, totalcash::float8::numeric::money,
    totaldebt::float8::numeric::money, shareholderequity::float8::numeric::money, cashchange::float8::numeric::money, operatinggainsandloses FROM 
    keyfinancials WHERE symbol = (%s)""", [slug])
    findata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    print('fin data from DB (API call first): ')
    self.write({'findata_db': findata_db})
    cur.close()
    conn.close()

def get_api_financials_cache(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("""SELECT to_char(reportdate, 'YYYY:MM:DD') as reportdate, grossprofit::float8::numeric::money, costofrevenue::float8::numeric::money, 
    operatingrevenue::float8::numeric::money, totalrevenue::float8::numeric::money, operatingincome::float8::numeric::money, netincome::float8::numeric::money,
    researchanddevelopment::float8::numeric::money, operatingexpense::float8::numeric::money, currentassets::float8::numeric::money, totalassets::float8::numeric::money,
    totalliabilities::float8::numeric::money, currentcash::float8::numeric::money, currentdebt::float8::numeric::money, totalcash::float8::numeric::money,
    totaldebt::float8::numeric::money, shareholderequity::float8::numeric::money, cashchange::float8::numeric::money, operatinggainsandloses FROM 
    keyfinancials WHERE symbol = (%s)""", [slug])
    findata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    print('fin data from DB (cache): ')
    findata_json = json.dumps(findata_db)
    self.write(findata_json)
    cur.close()
    conn.close()


def get_api_stats(self, slug):
    print('requesting API for key stats')
    r = requests.get('https://api.iextrading.com/1.0/stock/'+ slug + '/stats')
    statsdata = r.json()
    statsdata_list = []
    statsdata_list.append(statsdata)
    dt = datetime.utcnow()
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM keystats WHERE symbol = (%s)", [slug])
    for stats in statsdata_list:
        cur.execute("""INSERT INTO keystats VALUES (DEFAULT,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (dt, stats['companyName'], stats['marketcap'], stats['beta'], stats['week52high'], stats['week52low'], stats['week52change'], stats['dividendRate'], 
        stats['dividendYield'], stats['latestEPS'], stats['latestEPSDate'], stats['sharesOutstanding'], stats['returnOnEquity'], 
        stats['consensusEPS'], stats['symbol'], stats['EBITDA'], stats['revenue'], stats['grossProfit'], stats['cash'], stats['debt'], stats['ttmEPS'], 
        stats['revenuePerShare'], stats['peRatioHigh'], stats['peRatioLow'], stats['returnOnAssets'], stats['returnOnCapital'], stats['profitMargin'], 
        stats['priceToSales'], stats['priceToBook']))
        conn.commit()
    cur.execute("""SELECT marketcap::float8::numeric::money, beta, week52high, week52low, week52change, dividendrate, dividendyield, latesteps, to_char(latestepsdate, 'YYYY:MM:DD'), 
    sharesoutstanding, returnonequity, concensuseps, ebitda::float8::numeric::money, revenue::float8::numeric::money, grossprofit::float8::numeric::money,
    cash::float8::numeric::money, debt::float8::numeric::money, ttmeps, revenuepershare, peratiohigh, peratiolow, returnonassets, returnoncapital, 
    profitmargin, pricetosales, pricetobook FROM keystats WHERE symbol = (%s)""", [slug])
    statsdata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    print('stats data from DB (API call first): ')
    self.write({'statsdata_db': statsdata_db})
    cur.close()
    conn.close()


def get_api_stats_cache(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("""SELECT marketcap::float8::numeric::money, beta, week52high, week52low, week52change, dividendrate, dividendyield, latesteps, to_char(latestepsdate, 'YYYY:MM:DD'), 
    sharesoutstanding, returnonequity, concensuseps, ebitda::float8::numeric::money, revenue::float8::numeric::money, grossprofit::float8::numeric::money,
    cash::float8::numeric::money, debt::float8::numeric::money, ttmeps, revenuepershare, peratiohigh, peratiolow, returnonassets, returnoncapital, 
    profitmargin, pricetosales, pricetobook FROM keystats WHERE symbol = (%s)""", [slug])
    statsdata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    print('stats data from DB (cache): ')
    self.write({'statsdata_db': statsdata_db})
    cur.close()
    conn.close()


def get_api_news(self, slug):
    print('requesting API for company news')
    r = requests.get('https://api.iextrading.com/1.0/stock/'+ slug + '/news/last/50')
    newsdata = r.json()
    dt = datetime.utcnow()
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM companynews WHERE symbol = (%s)", [slug])
    for report in newsdata:
        cur.execute("""INSERT INTO companynews VALUES (DEFAULT,%s, %s, %s, %s, %s, %s, %s, %s)""",
        (slug, dt, report['datetime'], report['headline'], report['source'], report['url'], report['summary'], report['image']))
        conn.commit()
    cur.execute("""SELECT to_char(newsdate, 'YYYY:MM:DD') as newsdate, headline, source, url, summary FROM companynews WHERE symbol = (%s)""", [slug])
    newsdata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    newsdata_json = json.dumps(newsdata_db)
    self.write(newsdata_json)
    cur.close()
    conn.close()

def get_api_news_cache(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("""SELECT to_char(newsdate, 'YYYY:MM:DD') as newsdate, headline, source, url, summary FROM companynews WHERE symbol = (%s)""", [slug])
    newsdata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    newsdata_json = json.dumps(newsdata_db)
    self.write(newsdata_json)
    cur.close()
    conn.close()


def get_api_main(self, slug):
    print('requesting API for company main info')
    r = requests.get('https://api.iextrading.com/1.0/stock/'+ slug + '/company')
    maininfodata = r.json()
    maindata_list = []
    maindata_list.append(maininfodata)
    dt = datetime.utcnow()
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM companymaininfo WHERE symbol = (%s)", [slug])
    for report in maindata_list:
        cur.execute("""INSERT INTO companymaininfo VALUES (DEFAULT,%s, %s, %s, %s, %s, %s, %s, %s)""",
        (slug, dt, report['website'], report['industry'], report['exchange'], report['CEO'], report['sector'], report['description']))
        conn.commit()
    cur.execute("""SELECT website, industry, exchange, ceo, sector, description FROM companymaininfo WHERE symbol = (%s)""", [slug])
    maindata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    maindata_json = json.dumps(maindata_db)
    self.write(maindata_json)
    cur.close()
    conn.close()

def get_api_main_cache(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("""SELECT website, industry, exchange, ceo, sector, description FROM companymaininfo WHERE symbol = (%s)""", [slug])
    maindata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    maindata_json = json.dumps(maindata_db)
    self.write(maindata_json)
    cur.close()
    conn.close()






def get_api_ddm(self, slug):
    print('requesting API for company main info')
    r = requests.get('https://api.iextrading.com/1.0/stock/'+ slug + '/company')
    maininfodata = r.json()
    maindata_list = []
    maindata_list.append(maininfodata)
    dt = datetime.utcnow()
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("DELETE FROM companymaininfo WHERE symbol = (%s)", [slug])
    for report in maindata_list:
        cur.execute("""INSERT INTO companymaininfo VALUES (DEFAULT,%s, %s, %s, %s, %s, %s, %s, %s)""",
        (slug, dt, report['website'], report['industry'], report['exchange'], report['CEO'], report['sector'], report['description']))
        conn.commit()
    cur.execute("""SELECT website, industry, exchange, ceo, sector, description FROM companymaininfo WHERE symbol = (%s)""", [slug])
    maindata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    maindata_json = json.dumps(maindata_db)
    self.write(maindata_json)
    cur.close()
    conn.close()

def get_api_ddm_cache(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("""SELECT website, industry, exchange, ceo, sector, description FROM companymaininfo WHERE symbol = (%s)""", [slug])
    maindata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    maindata_json = json.dumps(maindata_db)
    self.write(maindata_json)
    cur.close()
    conn.close()