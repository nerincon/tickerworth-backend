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