import requests
from bs4 import BeautifulSoup as bs

import lxml.html

from random import choice


def get_useragent():
    useragent = open('res/useragent.list').read().split('\n')
    return {'User-Agent': choice(useragent)}


def get_html(url, method=None):
    # t = uniform(6, 18)
    # sleep(t)

    # Получаем новый user-agent
    useragent = get_useragent()
    proxy = None

    with requests.Session() as s:
        try:
            response = s.get(url=url, headers=useragent, proxies=proxy)
            if response.status_code == requests.codes.ok:
                # xsoup = lxml.html.document_fromstring(response.text)
                soup = bs(response.text, 'lxml')
                s.close()
                response.close()
                return response.status_code, soup
        except:
            print("Error " + str(response.status_code))
            return response.status_code, ''
