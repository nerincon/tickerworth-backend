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
    print('fin data from DB (API call first): ', findata_db)
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
    print('fin data from DB (cache): ', findata_db)
    self.write({'findata_db': findata_db})
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
        cur.execute("""INSERT INTO keystats VALUES (DEFAULT,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (dt, stats['companyName'], stats['marketcap'], stats['beta'], stats['week52high'], stats['week52low'], stats['week52change'], stats['dividendRate'], 
        stats['dividendYield'], stats['exDividendDate'], stats['latestEPS'], stats['latestEPSDate'], stats['sharesOutstanding'], stats['returnOnEquity'], 
        stats['consensusEPS'], stats['symbol'], stats['EBITDA'], stats['revenue'], stats['grossProfit'], stats['cash'], stats['debt'], stats['ttmEPS'], 
        stats['revenuePerShare'], stats['peRatioHigh'], stats['peRatioLow'], stats['returnOnAssets'], stats['returnOnCapital'], stats['profitMargin'], 
        stats['priceToSales'], stats['priceToBook']))
        conn.commit()
    cur.execute("""SELECT marketcap, beta, week52high, week52low, week52change, dividendrate, dividendyield, to_char(exdividenddate, 'YYYY:MM:DD'), latesteps, to_char(latestepsdate, 'YYYY:MM:DD'), 
    sharesoutstanding, returnonequity, concensuseps, ebitda::float8::numeric::money, revenue::float8::numeric::money, grossprofit::float8::numeric::money,
    cash::float8::numeric::money, debt::float8::numeric::money, ttmeps, revenuepershare, peratiohigh, peratiolow, returnonassets, returnoncapital, 
    profitmargin, pricetosales, pricetobook FROM keystats WHERE symbol = (%s)""", [slug])
    statsdata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    print('stats data from DB (API call first): ', statsdata_db)
    self.write({'statsdata_db': statsdata_db})
    cur.close()
    conn.close()


def get_api_stats_cache(self, slug):
    conn = psycopg2.connect("dbname=tickerworth user=postgres")
    cur = conn.cursor()
    cur.execute("""SELECT marketcap, beta, week52high, week52low, week52change, dividendrate, dividendyield, to_char(exdividenddate, 'YYYY:MM:DD'), latesteps, to_char(latestepsdate, 'YYYY:MM:DD'), 
    sharesoutstanding, returnonequity, concensuseps, ebitda::float8::numeric::money, revenue::float8::numeric::money, grossprofit::float8::numeric::money,
    cash::float8::numeric::money, debt::float8::numeric::money, ttmeps, revenuepershare, peratiohigh, peratiolow, returnonassets, returnoncapital, 
    profitmargin, pricetosales, pricetobook FROM keystats WHERE symbol = (%s)""", [slug])
    statsdata_db = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
    print('stats data from DB (cache): ', statsdata_db)
    self.write({'statsdata_db': statsdata_db})
    cur.close()
    conn.close()