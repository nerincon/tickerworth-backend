# from datetime import datetime, timedelta
# import os
# import psycopg2
# import json

# currentMonth = datetime.now().month
# print(currentMonth)
# currentYear = datetime.now().year
# print(currentYear)
# currentDay = datetime.now().day
# print(currentDay)


# env = os.environ.get("PYTHON_ENV")
# if env == "production":
#    print("I'm in production")
# else:
#     print('In Dev mode')

# logo = ('https://storage.googleapis.com/iex/api/logos/AAPL.png',)

# logo_dict = {'url': x for x in logo}

# print(logo[0])

# print(logo_dict)

# timeDelta = timedelta(minutes=1440)
# print(timeDelta)
# conn = psycopg2.connect("dbname=tickerworth user=postgres")
# cur = conn.cursor()
# cur.execute("SELECT to_char(reportdate, 'YYYY:MM:DD') as x, grossprofit as y FROM keyfinancials  WHERE symbol = 'AAPL'")
# pulleddata = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
# data_json = json.dumps(pulleddata)
# print(data_json)
# cur.close()
# conn.close()

import pandas as pd
import requests

ticker = 'AAPL'

r_1 = requests.get('https://api.iextrading.com/1.0/stock/aapl/dividends/5y')
divdata = r_1.json()
r_2 = requests.get('https://api.iextrading.com/1.0/stock/aapl/splits/5y')
splits = r_2.json()
splits_length = len(splits)
if splits_length > 1:
    print('More than 1 split in 5 years!. Will not calculate DDM')
else:
    # print(divdata)
    split_date = splits[0]['declaredDate']
    ratio = splits[0]['ratio']
    dividends = []
    for x in divdata:
        if x['declaredDate'] <= split_date:
            new_amount = x['amount'] * ratio
            dividends.append(new_amount)
        else:
            dividends.append(x['amount'])
    # print(dividends)

rev_dividends = dividends[::-1]

declared_dates = []
for r in divdata:
    declared_dates.append(r['declaredDate'])

rev_declared_dates = declared_dates[::-1]

df = pd.DataFrame({
    ticker: rev_dividends},
    index=rev_declared_dates)
# print(df)
pc = df.pct_change()

mylist = list(pc[ticker].values)
mylistfinal = mylist.pop(0)
# print(mylist)

quarterly_growth_rate = (sum(mylist)/len(mylist)) * 100
annual_growth_rate = (quarterly_growth_rate ** 3) / 100
# print(annual_growth_rate)



r_3 = requests.get('https://www.quandl.com/api/v3/datasets/USTREASURY/YIELD.json?api_key=gvcTKFWqWYJ5tD2Y--q7&start_date=2018-08-15')
us_treasury_data = r_3.json()
treasury_rate = us_treasury_data['dataset']['data'][0][9]
treasury_rate_adjusted = treasury_rate/100


# using the average annualized total return for the S&P 500 index over the past 5 years (july-2013-august-2018), which is 10.98% percent. No API for this.
sp500 = 0.1098

r_4 = requests.get('https://api.iextrading.com/1.0/stock/aapl/stats')
stats_data = r_4.json()
beta = stats_data['beta']
r_5 = requests.get('https://api.iextrading.com/1.0/stock/aapl/stats')
comp_data = r_5.json()
div_rate = comp_data['dividendRate']


market_premium = sp500 - treasury_rate_adjusted
company_premium = beta * market_premium

capm = treasury_rate_adjusted + company_premium
print('capm: ',capm)
print('growth_rate' , annual_growth_rate)

numerator = div_rate * (1 + annual_growth_rate)
print('numerator: ', numerator)
denominator = capm - annual_growth_rate
print('denominator: ', denominator)
ddm_valuation = (div_rate * (1 + annual_growth_rate)) / (capm - annual_growth_rate)
print('ddm valuation: ' , ddm_valuation)

