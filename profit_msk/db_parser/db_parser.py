import re
import os

import pandas
from utils import db_utils


def start():
    for root, dirnames, filenames in os.walk(os.path.join("profit_msk", "parse")):
        for file in filenames:
            if file.endswith("_parts.csv"):
                print()
                print(file)

                fn = os.path.join(root, file)
                try:
                    data = pandas.read_csv(fn, sep=';', header=None)
                    data = data.values.tolist()
                except:
                    data = []
                for d in data:
                    brand_id = 0
                    part_id = 0

                    if str(d[0]) != 'nan':
                        brand_id = db_utils.get_brand_id(d[0])
                        print(d[0], end='; ')
                    if str(d[1]) != 'nan':
                        # print(db_utils.get_spr_modules_ru(d[1]), d[1], end='; ')
                        print(d[1], end='; ')
                    if str(d[2]) != 'nan':
                        print(d[2])

                        part_id = db_utils.get_part_code_id(d[2])
                        if not part_id:
                            spr_detail_id = db_utils.add_spr_details(d[3], d[4])
                            part_id = db_utils.add_partcode(brand_id, d[2], d[7], spr_detail_id)
                        else:
                            spr_detail_id = db_utils.add_spr_details(d[3], d[4])
                            db_utils.update_partcode(brand_id, part_id, d[7], spr_detail_id)
                        model_id = db_utils.get_model_id(file.replace('_parts.csv', ''))
                        if part_id and model_id:
                            spr_modules_id = db_utils.get_modules_id(part_id, model_id)
                            if spr_modules_id:
                                for spr_module_id in spr_modules_id:
                                    db_utils.update_module(spr_module_id[0], d[1])
                            else:
                                spr_module_id = db_utils.add_module(d[1])
                                db_utils.add_details(part_id, model_id, spr_module_id)
                        else:
                            print('ERROR:', file)
                            df = pandas.DataFrame([f"{file}"], )
                            df.to_csv('error_files.csv', index=False, mode='a', header=False, sep=";")
                            break
                        print(d[2], end='; ')
                    else:
                        print()
                    if str(d[3]) != 'nan':
                        print(d[3], end='; ')
                    if str(d[4]) != 'nan':
                        print(d[4], end='; ')
                    if str(d[5]) != 'nan':
                        print(d[5], end='; ')
                    if str(d[6]) != 'nan':
                        d[6] = int(fix_price(d[6]))
                        db_utils.add_prices(d[6], 2, part_id)
                        print(d[6], end='; ')
                    if str(d[7]) != 'nan':
                        print(d[7])
                    else:
                        print()


def fix_price(old_price):
    price = str(int(old_price))
    if len(price) == 2 or len(price) == 3:
        old_price = re.sub(r'\d$', '0', price)
    if len(price) == 3:
        t_price = re.sub(r'\d$', '', price)
        if int(t_price) > 50:
            if int(re.search(r'\d$', t_price).group(0)) > 5:
                price = re.sub(r'\d.$', '50', price)
            else:
                price = re.sub(r'\d.$', '00', price)
            old_price = int(price)
        else:
            old_price = re.sub(r'\d$', '0', price)
    elif len(price) == 4 or len(price) == 5:
        old_price = re.sub(r'\d.$', '00', price)
    elif len(price) >= 6:
        old_price = re.sub(r'\d..$', '000', price)
    return old_price


def linked_partcode_spr_diteils_is_null():
    parts_list = db_utils.get_all_partcode_spr_details_is_null()
    for part_id in parts_list:
        if part_id:
            print('partcode_id:', part_id[0])
            brand_id = 0
            model_id = 0
            spr_detail_id = 0
            try:
                d = db_utils.get_spr_detail_id_in_details(part_id[0])
                spr_detail_id = d[0][1]
                if spr_detail_id:
                    model_id = d[0][0]
                    if model_id:
                        brand_id = db_utils.get_brand_id_in_models(model_id)
                        db_utils.linked_partcode(part_id[0], brand_id, spr_detail_id)
            except:
                print('partcode_id:', part_id[0], ', brand_id:', brand_id, ', model_id:', model_id,
                      ', spr_detail_id:', spr_detail_id, ' --- ERROR')


def generate_article_partcode():
    s = ''
    art = 'P400000000'
    parts_list = db_utils.get_ids('partcodes')
    for n, i in enumerate(parts_list):
        n = n + 1
        if n <= 9:
            s = re.sub(rf'\d$', str(n), art)
        elif (n >= 10) and (n <= 99):
            s = re.sub(rf'\d.$', str(n), art)
        elif (n >= 100) and (n <= 999):
            s = re.sub(rf'\d..$', str(n), art)
        elif (n >= 1000) and (n <= 9999):
            s = re.sub(rf'\d...$', str(n), art)
        elif (n >= 10000) and (n <= 99999):
            s = re.sub(rf'\d....$', str(n), art)
        elif (n >= 100000) and (n < 999999):
            s = re.sub(rf'\d.....$', str(n), art)
        elif n >= 1000000:
            s = re.sub(rf'\d......$', str(n), art)
        print(i[0], s)
        db_utils.add_partcode_article(i[0], s)

