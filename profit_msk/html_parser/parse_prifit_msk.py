import os
import pandas
from selenium import webdriver

from profit_msk.html_parser.model_parser import ModelParser
import webdriver_options

options = webdriver_options.set_options()
driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)


def model_parse():
    # urls = [['brother', 'https://profit-msk.ru/brother/brother/brother.html'],
    #         ['canon', 'https://profit-msk.ru/canon/zip/index.html'],
    #         ['hp', 'https://profit-msk.ru/hp/zip/index.html'],
    #         ['epson', 'https://profit-msk.ru/epson/epson/index.html'],
    #         ['konica-minolta', 'https://profit-msk.ru/konica-minolta/konica-minolta/konica-minolta.html'],
    #         ['kyocera', 'https://profit-msk.ru/kyocera-mita/zip/index.html'],
    #         ['lexmark', 'https://profit-msk.ru/lexmark/spareparts/index.html'],
    #         ['oki', 'https://profit-msk.ru/oki/zip/index.html'],
    #         ['ricoh', 'https://profit-msk.ru/ricoh/ricoh/ricoh.html'],
    #         ['samsung', 'https://profit-msk.ru/samsung/zip/index.html'],
    #         ['sharp', 'https://profit-msk.ru/sharp/sharp/sharp.html'],
    #         ['xerox', 'https://profit-msk.ru/xerox/zip/index.html']]
    #
    # parser = ModelLinks(driver, urls)
    # models_urls = parser.get_links_model()
    # base_path = os.path.join('profit_msk', 'parse')
    #
    # df = pandas.DataFrame(models_urls)
    # df.to_csv(os.path.join(base_path, 'urls.csv'), index=False, mode='a',
    #           encoding='utf-8', header=False, sep=";")

    model_parser = ModelParser(driver, load_urls_list())
    model_parser.parse_model()


def load_urls_list():
    base_path = os.path.join('profit_msk', '../parse')
    models_urls = pandas.read_csv(os.path.join(base_path, 'urls.csv'), sep=';', header=None)
    models_urls = models_urls.values.tolist()
    return models_urls
