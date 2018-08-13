CREATE TABLE companylist (
  id SERIAL NOT NULL PRIMARY KEY,
  symbol VARCHAR,
  name VARCHAR,
  pulldate date,
  iextype VARCHAR,
  iexid VARCHAR
);

-- SELECT EXTRACT(YEAR FROM pulldate) as year, EXTRACT(MONTH FROM pulldate) as month, EXTRACT(DAY FROM pulldate) as day FROM companylist WHERE id = 1

-- DELETE FROM companylist

CREATE TABLE keystats (
  id SERIAL NOT NULL PRIMARY KEY,
  companyname VARCHAR,
  marketcap INTEGER,
  beta DECIMAL,
  week52high DECIMAL,
  week52low DECIMAL,
  week52change DECIMAL,
  dividendrate DECIMAL,
  dividendyield DECIMAL,
  exdividenddate DATE,
  latesteps DECIMAL,
  latestepsdate DATE,
  sharesoutstanding INTEGER,
  returnonequity DECIMAL,
  concensuseps DECIMAL,
  symbol VARCHAR,
  ebitda INTEGER,
  revenue INTEGER,
  grossprofit INTEGER,
  cash INTEGER,
  debt INTEGER,
  ttmeps DECIMAL,
  revenuepershare DECIMAL,
  peratiohigh DECIMAL,
  peratiolow DECIMAL,
  returnonassets DECIMAL,
  returnoncapital DECIMAL,
  profitmargin DECIMAL,
  pricetosales DECIMAL,
  pricetobook DECIMAL
);

CREATE TABLE keyfinancials (
  id SERIAL NOT NULL PRIMARY KEY,
  symbol VARCHAR,
  reportdate DATE,
  grossprofit INTEGER,
  costofrevenue INTEGER,
  operatingrevenue INTEGER,
  totalrevenue INTEGER,
  operatingincome INTEGER,
  netincome INTEGER,
  researchanddevelopment INTEGER,
  operatingexpense INTEGER,
  currentassets INTEGER,
  totalassets INTEGER,
  totalliabilities INTEGER,
  currentcash INTEGER,
  currentdebt INTEGER,
  totalcash INTEGER,
  totaldebt INTEGER,
  shareholderequity INTEGER,
  cashchange INTEGER,
  cashflow INTEGER,
  operatinggainsandloses INTEGER
);

CREATE TABLE companyimage (
  id SERIAL NOT NULL PRIMARY KEY,
  symbol VARCHAR,
  url VARCHAR
);