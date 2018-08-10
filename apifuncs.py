import requests
import json
from pprint import pprint


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


