CREATE TABLE companylist (
  id SERIAL NOT NULL PRIMARY KEY,
  symbol VARCHAR,
  name VARCHAR,
  pulldate date,
  iextype VARCHAR,
  iexid VARCHAR
);

-- SELECT EXTRACT(YEAR FROM pulldate) as year, EXTRACT(MONTH FROM pulldate) as month, EXTRACT(DAY FROM pulldate) as day FROM companylist WHERE id = 1