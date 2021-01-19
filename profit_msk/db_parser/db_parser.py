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
                        part_id = db_utils.get_part_code_id(d[2])
                        spr_detail_id = db_utils.add_spr_details(d[3], d[4])
                        if not part_id:
                            part_id = db_utils.add_partcode(brand_id, d[2], d[7], spr_detail_id)
                        else:
                            db_utils.update_partcode(brand_id, part_id, d[7], spr_detail_id)
                        # model_id = db_utils.get_model_id(re.sub('_parts\.csv', '', file))
                        if part_id: # and model_id:
                            pass
                            # module_id = db_utils.get_module_id_details(part_id, model_id)
                            # if not module_id:
                            #     module_id = db_utils.add_module(d[1])
                            #     spr_detail_id = db_utils.get_spr_details(d[3], d[4])
                            #     if spr_detail_id:
                            #         db_utils.update_spr_details(spr_detail_id, d[3], d[4])
                            #     else:
                            #         spr_detail_id = db_utils.add_spr_details(d[3], d[4])
                            #     if part_id and model_id and module_id and spr_detail_id:
                            #         db_utils.add_details(part_id, model_id, module_id, spr_detail_id)
                            #     else:
                            #         print('ERROR:', file)
                            #         print(d)
                            #         break
                            # else:
                            #     db_utils.update_module(module_id, d[1])
                            #     spr_detail_id = db_utils.get_details_spr_details(part_id, model_id, module_id)
                            #     if spr_detail_id:
                            #         db_utils.update_spr_details(spr_detail_id, d[3], d[4])
                            #     else:
                            #         spr_detail_id = db_utils.get_spr_details(d[3], d[4])
                            #         db_utils.add_details(part_id, model_id, module_id, spr_detail_id)
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
            # break
    # break


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
