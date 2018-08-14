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
  marketcap BIGINT,
  beta DECIMAL,
  week52high DECIMAL,
  week52low DECIMAL,
  week52change DECIMAL,
  dividendrate DECIMAL,
  dividendyield DECIMAL,
  exdividenddate DATE,
  latesteps DECIMAL,
  latestepsdate DATE,
  sharesoutstanding BIGINT,
  returnonequity DECIMAL,
  concensuseps DECIMAL,
  symbol VARCHAR,
  ebitda BIGINT,
  revenue BIGINT,
  grossprofit BIGINT,
  cash BIGINT,
  debt BIGINT,
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
  time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  reportdate DATE,
  grossprofit BIGINT,
  costofrevenue BIGINT,
  operatingrevenue BIGINT,
  totalrevenue BIGINT,
  operatingincome BIGINT,
  netincome BIGINT,
  researchanddevelopment BIGINT,
  operatingexpense BIGINT,
  currentassets BIGINT,
  totalassets BIGINT,
  totalliabilities BIGINT,
  currentcash BIGINT,
  currentdebt BIGINT,
  totalcash BIGINT,
  totaldebt BIGINT,
  shareholderequity BIGINT,
  cashchange BIGINT,
  cashflow BIGINT,
  operatinggainsandloses BIGINT
);

CREATE TABLE companyimage (
  id SERIAL NOT NULL PRIMARY KEY,
  symbol VARCHAR,
  url VARCHAR
);