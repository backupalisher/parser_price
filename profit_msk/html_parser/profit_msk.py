import re

from utils import db_utils
from utils import http
from utils import other_utils


def start():
    # Получить ссылки нулевого уровня
    vendor = 'profit-msk'
    # add_brands_links_db(vendor, 0)
    # add_models_links_db(vendor, 1)
    # add_model_data_links_db(vendor, 2)
    brand_name, model_name, device_spec, device_data, supplies_data = \
        model_parser(get_data_html('https://profit-msk.ru/canon/zip/i-sensys-lbp3310.html'), 'Canon')

    print(brand_name)
    print(model_name)
    print(device_spec)
    print(device_data)
    print(supplies_data)


def get_links_db(vendor, level):
    vendor_id = db_utils.get_vendor_id(vendor)
    links = db_utils.get_point_links(vendor_id, level)
    return vendor_id, links


def get_brands_link(soup):
    brands_link = []
    brands = soup.find_all('div', class_='spotlight')
    for brand in brands:
        href = re.sub(r'(^..+?(?==)..)|(.$)', '', brand['onclick'])
        brands_link.append(
            href
        )
    return brands_link


def get_data_html(url):
    status_code, soup = http.get_html(url)
    if status_code == 200:
        return soup


def add_brands_links_db(vendor, level):
    # Получаем все ссылки {vendor} и {level}
    vendor_id, links = get_links_db(vendor, level)

    # Получить ссылки всех брендов и записать в БД, задаем уровень ссылок 1
    for url in links:
        if url[0]:
            url = url[0]
            brand_links = get_data_html(url)
            if brand_links:
                for link in brand_links:
                    print(link)
                    link = other_utils.check_http(link, url)
                    db_utils.insert_link(vendor_id, link, 1, None)


def get_models_links(soup):
    models_links = []
    models = soup.find_all('div', class_='tbltsttt')
    for model in models:
        href = re.sub(r'(^..+?(?==)..)|(.$)', '', model['onclick'])
        brand_name = re.search(r'^.+?(?=/).', href).group(0)
        brand_name = re.sub(r'\W', '', brand_name)
        models_links.append([
            brand_name,
            'https://profit-msk.ru' + href,
        ])
    return models_links


def add_models_links_db(vendor, level):
    # Получаем все ссылки {vendor} и {level}
    vendor_id, links = get_links_db(vendor, level)

    # Получить ссылки всех моделей и записать в БД, задаем второй уровень ссылок
    for url in links:
        if url[0]:
            url = url[0]
            models_links = get_data_html(url)
            if models_links:
                for link in models_links:
                    print(link)
                    new_link = other_utils.check_http(link[1], url)
                    db_utils.insert_link(vendor_id, new_link, 2, link[0])


def model_parser(soup, brand_name):
    full_data = soup.find('div', class_='full-article')
    model_name = full_data.find('span').text
    print(model_name)
    device_spec = []
    supplies_data = []

    try:
        img_url = full_data.find('a', title=model_name)['href']
        # model_image = save_image.save_img('https://profit-msk.ru' + img_url, brand_name, model_name)
        # if model_image:
        #     device_spec.append(['model_image', model_image])
    except:
        pass

    table_body = full_data.find_next('table')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [re.sub(r'\n|\r', ' ', ele.text.strip()) for ele in cols]
        for i, col in enumerate(cols[2:]):
            if i % 2 == 0:
                device_spec.append([col, cols[i + 3]])

    data = full_data.find_all('div', class_='jwts_tabbertab')

    tables = data[0].find_all('table', cellspacing='0')
    device_data = []
    products_analogs = []
    module_name = ''
    part_code = ''
    part_name = ''
    vendor = ''
    old_part_code = None

    # ЗИП
    for table in tables[1:]:
        models_list = []
        part_image = ''
        try:
            module_name = table.find('td', attrs={'class': 'zip_t_caption brdimg', 'colspan': '4'}).text
            continue
        except:
            pass

        # Проверка на наличие аналогов
        try:
            if table.find('td', class_='zancap'):
                old_part_code = part_code

            if old_part_code:
                part_code = table.find('span', class_='pbld').text
                products_analogs.append({
                    'product_id': old_part_code,
                    'product_analog_id': part_code,
                })
        except:
            old_part_code = ''

        try:

            # My_table = soup.find('table', {'class': 'wikitable sortable'})
            # My_row = My_table.find_all('tr')
            # for row in My_row:
            #     data = row.find_next('td').find_next('td')
            #     print(data.text.strip())

            table_row = table.find_all('tr', class_='bcgrndclr')

            for row in table_row:
                cols = row.find_all('td')
                print(cols[0].text)
                print(cols[1].text)
                print(cols[2].text)
                print(cols[3].text)
                print(cols[4].text)
                # // *[ @ id = "zzzzzzzzzz"] / table / tbody / tr[3] / td[4]
                # for col in cols:
                #     print(col.text)
                # table_td = table_row.find_all('td')
                # vendor = table.find('td', class_='brdimg').text.strip()

                # //*[@id="jwts_tab"]/div[1]/div/table[3]/tbody/tr/td[1]
                #- vendor = row.find('td').text.replace('• ', '').sprip()
                # part_code = table.find('span', class_='pbld').text
                #-part_code = row.find('span', class_='pbld').text
                # part_names = table.find_all('tr', class_='bcgrndclr')
                #-part_name = row.find('td')[1].text.strip()
                #-part_name = re.sub(rf'\n|\r|{part_code}', '', part_name).strip()
                #-part_name = re.sub(rf'^-', '', part_name).strip()
                #-part_price = re.sub(r'\u20cf', '', row.text).strip()
                #-part_price = int(re.sub(r'\u20cf', '', row.text).strip())
        except:
            part_price = 0

        # try:
            # img_url = full_data.find('a', title=part_code)['href']
            # part_image = save_image.save_img('https://profit-msk.ru' + img_url, brand_name, part_code)
        # except:
        #     pass
        try:
            models = table.find_all('td', class_='tztdclass')
            for model in models[1:]:
                if model.text:
                    models_list.append(model.text)
        except:
            pass
        if module_name and part_code:
            device_data.append({
                'vendor': vendor,
                'module': module_name,
                'part_code': part_code,
                'part_name': part_name,
                'models_list': models_list,
                'part_image': part_image,
                'part_price': part_price,
            })
    # Расходные материалы
    tables = data[1].find_all('table')
    for table in tables:
        supplies = table.find_all('span', class_='pbld')
        for model in supplies:
            try:
                supplies_name = model.find('a').text
                supplies_url = model.find('a')['href']
            except:
                supplies_name = ''
                supplies_url = ''

            if supplies_url:
                supplies_data.append({
                    'supplies_name': supplies_name,
                    'supplies_url': 'https://profit-msk.ru' + supplies_url,
                })

    return brand_name, model_name, device_spec, device_data, supplies_data


def add_model_data_links_db(vendor, level):
    vendor_id, links = get_links_db(vendor, level)
    # Получить ссылки всех моделей и записать в БД, задаем третий уровень ссылок
    for url in links:
        if url[0]:
            url = url[0]
        model_parts_links = get_data_html(url)
        if model_parts_links:
            for link in model_parts_links:
                print(link)
                new_link = other_utils.check_http(link[1], url)
                db_utils.insert_link(vendor_id, new_link, 3, link[0])


# def supplies_parser(soup, )
