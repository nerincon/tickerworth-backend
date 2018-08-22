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
  time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  companyname VARCHAR,
  marketcap BIGINT,
  beta DOUBLE PRECISION,
  week52high DOUBLE PRECISION,
  week52low DOUBLE PRECISION,
  week52change DOUBLE PRECISION,
  dividendrate DOUBLE PRECISION,
  dividendyield DOUBLE PRECISION,
  latesteps DOUBLE PRECISION,
  latestepsdate DATE,
  sharesoutstanding BIGINT,
  returnonequity DOUBLE PRECISION,
  concensuseps DOUBLE PRECISION,
  symbol VARCHAR,
  ebitda BIGINT,
  revenue BIGINT,
  grossprofit BIGINT,
  cash BIGINT,
  debt BIGINT,
  ttmeps DOUBLE PRECISION,
  revenuepershare INTEGER,
  peratiohigh DOUBLE PRECISION,
  peratiolow DOUBLE PRECISION,
  returnonassets DOUBLE PRECISION,
  returnoncapital DOUBLE PRECISION,
  profitmargin DOUBLE PRECISION,
  pricetosales DOUBLE PRECISION,
  pricetobook DOUBLE PRECISION
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

CREATE TABLE companyprice (
  id SERIAL NOT NULL PRIMARY KEY,
  symbol VARCHAR,
  price DOUBLE PRECISION
);

CREATE TABLE companyddm (
  id SERIAL NOT NULL PRIMARY KEY,
  symbol VARCHAR,
  time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ddm DOUBLE PRECISION
);

CREATE TABLE companynews (
  id SERIAL NOT NULL PRIMARY KEY,
  symbol VARCHAR,
  time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  newsdate DATE,
  headline VARCHAR,
  source VARCHAR,
  url VARCHAR,
  summary VARCHAR,
  image VARCHAR
);

CREATE TABLE companymaininfo (
  id SERIAL NOT NULL PRIMARY KEY,
  symbol VARCHAR,
  time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  website VARCHAR,
  industry VARCHAR,
  exchange VARCHAR,
  ceo VARCHAR,
  sector VARCHAR,
  description VARCHAR
);