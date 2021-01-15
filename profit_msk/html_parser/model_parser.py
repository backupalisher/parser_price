import os
import re

import pandas
from random import uniform
from time import sleep

from profit_msk.html_parser.save_image_url import save_image_url


class ModelParser(object):
    def __init__(self, driver, urls):
        self.driver = driver
        self.urls = urls

    def parse_model(self):
        for url in self.urls:
            sleep(uniform(9, 18))
            self.driver.get(url[1])

            t_path = os.path.join('profit_msk', '../parse')
            base_path = os.path.join(t_path, url[0])
            if not os.path.exists(base_path):
                os.mkdir(base_path)

            try:
                model_name = self.driver.find_element_by_xpath('//*[@id="page"]/div[2]/strong/span').text
                model_name = re.sub('/', ' ', model_name)
                print(f'{model_name}...', end='')
            except:
                print(url[1])
                continue
            try:
                img_url = self.driver.find_element_by_xpath('//*[@id="page"]/table/tbody/tr/td[1]/center/a'). \
                    get_attribute("href")
            except:
                img_url = None

            # Скачиваем и сохраняем картинку
            options_list = save_image_url(img_url, base_path, model_name)

            options_table = self.driver.find_element_by_xpath('//*[@id="page"]/table/tbody/tr/td[2]/table/tbody').text
            options_text = str.splitlines(options_table)

            for l in options_text:
                nl = l.split(': ')
                options_list.append(nl)

            try:
                device_status = self.driver.find_element_by_xpath('//*[@id="page"]/pre/span').text
            except:
                device_status = None
            options_list.append(['Status', device_status])
            if options_list and model_name:
                df = pandas.DataFrame(options_list)

                df.to_csv(os.path.join(base_path, f'{model_name}_options.csv'), index=False, mode='a', encoding='utf-8',
                          header=False, sep=";")

            table_count = self.driver.find_elements_by_xpath('//*[@id="jwts_tab"]/div[1]/div/table')

            module_name = ''
            for i in range(2, len(table_count) + 1):
                brand_name = ''
                part_code = ''
                part_name = ''
                status = ''
                part_image = ''

                property_data = []

                try:
                    self.driver.find_element_by_xpath(f"//*[@id='jwts_tab']/div[1]/div/table[{i}]"
                                                      f"/tbody/tr/td[4]/div").click()
                except:
                    pass

                try:
                    t_module = self.driver.find_element_by_xpath(f"//*[@id='jwts_tab']/div[1]/div/table[{i}]"
                                                                 f"/tbody/tr/td[@class='zip_t_caption brdimg']").text
                    if t_module:
                        module_name = t_module.strip()
                        continue
                except:
                    pass

                try:
                    brand_name = self.driver.find_element_by_xpath(f"//*[@id='jwts_tab']/div[1]/div/table[{i}]"
                                                                   f"/tbody/tr/td[@class='brdimg']").text
                except:
                    pass

                try:
                    part_code = self.driver.find_element_by_xpath(f"//*[@id='jwts_tab']/div[1]/div/table[{i}]"
                                                                  f"/tbody/tr/td/strong/span[@class='pbld']").text
                except:
                    pass

                try:
                    part_img_url = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[1]/div/table[{i}]'
                                                                     f'/tbody/tr/td[3]/a').get_attribute("href")
                except:
                    part_img_url = None

                t_part_img = save_image_url(part_img_url, base_path, part_code)
                if t_part_img:
                    part_image = t_part_img[0][1]

                try:
                    t_part_name = ''
                    t_part_name = self.driver.find_element_by_xpath(f"//*[@id='jwts_tab']/div[1]/div/table[{i}]"
                                                                    f"/tbody/tr/td[2]").text
                    if t_part_name:
                        if part_code:
                            if part_code == 'Q2665-60125':
                                print()
                            part_name = re.sub(rf'{part_code}|^-', '', t_part_name).strip()
                        else:
                            part_name = t_part_name.strip()

                except:
                    pass

                try:
                    t_price = ''
                    t_price = self.driver.find_element_by_xpath(f"//*[@id='jwts_tab']/div[1]/div/table[{i}]"
                                                                f"/tbody/tr/td[4]").text
                    if t_price:
                        price = t_price
                    else:
                        price = self.driver.find_element_by_xpath(f"//*[@id='jwts_tab']/div[1]/div/table[{i}]"
                                                                  f"/tbody/tr/td[4]/span").text
                    price = re.sub(rf'[^\d]', '', price)
                except:
                    raise

                try:
                    if re.search(r'Снято с производства', part_name).group(0):
                        status = 'Снято с производства'
                        part_name = re.sub(r'\nСнято с производства', '', part_name)
                except:
                    status = None

                try:
                    content = re.search(r'---([^<]*)---', part_name).group(0)
                    content = re.sub(r'-{2,}|\u0020{2,}|\nСостав:\n', '', content).strip()
                except:
                    content = None

                part_name = re.sub(r'^-\u0020|\u0020{2,}|\nСостав:\n|\n{2,}|-{2,}|^\n|\n$', '', part_name).strip()

                if part_code or part_name or content:
                    property_data.append([brand_name.strip(), module_name.strip(), part_code.strip(), part_name.strip(),
                                          content, status, price, part_image])
                    df = pandas.DataFrame(property_data)

                    df.to_csv(os.path.join(base_path, f'{model_name}_parts.csv'), index=False, mode='a',
                              encoding='utf-8', header=False, sep=";")

                # print(brand_name.strip(), module_name.strip(), part_code.strip(), part_name.strip(),
                #                           content, status, price, part_image)

            supplies_table = self.driver.find_elements_by_xpath('//*[@id="jwts_tab"]/div[2]/div/table/tbody/tr')

            for i in range(2, len(supplies_table) + 1):
                try:
                    name = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[2]/div/table/tbody/'
                                                             f'tr[{i}]/td[1]/span/a').get_attribute("text")
                    url = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[2]/div/table/tbody/'
                                                            f'tr[{i}]/td[1]/span/a').get_attribute("href")
                except:
                    name = None
                    url = None
                try:
                    desc = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[2]/div/table/tbody/'
                                                             f'tr[{i}]/td[2]/a').get_attribute("text")
                except:
                    desc = None
                try:
                    refill = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[2]/div/table/tbody/'
                                                               f'tr[{i}]/td[4]/a').get_attribute("text")
                    refill = re.sub(r'[^\w\s-]|\s{2,}', '', refill)
                except:
                    refill = None
                try:
                    recovery = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[2]/div/table/tbody/'
                                                                 f'tr[{i}]/td[5]/a').get_attribute("text")
                    recovery = re.sub(r'[^\w\s-]|\s{2,}', '', recovery)
                except:
                    recovery = None
                try:
                    swap_chip = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[2]/div/table/tbody/'
                                                                  f'tr[{i}]/td[6]/a').get_attribute("text")
                    swap_chip = re.sub(r'[^\w\s-]|\s{2,}', '', swap_chip)
                except:
                    swap_chip = None
                try:
                    original = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[2]/div/table/tbody/'
                                                                 f'tr[{i}]/td[7]/a').get_attribute("text")
                    original = re.sub(r'[^\w\s-]|\s{2,}', '', original)
                except:
                    original = None
                try:
                    compatible = self.driver.find_element_by_xpath(f'//*[@id="jwts_tab"]/div[2]/div/table/tbody/'
                                                                   f'tr[{i}]/td[8]/a').get_attribute("text")
                    compatible = re.sub(r'[^\w\s-]|\s{2,}', '', compatible)
                except:
                    compatible = None

                # print(name, url, desc,
                #       re.sub(r'[^\w\s-]|\s{2,}', '', refill),
                #       re.sub(r'[^\w\s-]|\s{2,}', '', recovery),
                #       re.sub(r'[^\w\s-]|\s{2,}', '', swap_chip),
                #       re.sub(r'[^\w\s-]|\s{2,}', '', original),
                #       re.sub(r'[^\w\s-]|\s{2,}', '', compatible))

                supplies_data = []
                if name or url or desc:
                    supplies_data.append([name, url, desc, refill, recovery, swap_chip, original, compatible])
                    df = pandas.DataFrame(supplies_data)

                    df.to_csv(os.path.join(base_path, f'{model_name}_supplies.csv'), index=False, mode='a',
                              encoding='utf-8', header=False, sep=";")
            print(f'\r{model_name}')
