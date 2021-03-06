from utils import db


def insert_link(vendor_id, url, point, brand):
    q = db.i_request(f"WITH s as (SELECT id FROM site_links "
                     f"WHERE url = '{url}'), i as "
                     f"(INSERT INTO site_links (vendor_id, url, point, brand) SELECT {vendor_id}, '{url}', {point}, '{brand}' "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    if q:
        return q[0][0]
    else:
        return 0


"""
_query(f'INSERT INTO prices (price, model_id, vendor_id) VALUES ({price}, {id}, {vendor}) '
       f'ON CONFLICT (vendor_id, model_id) DO UPDATE SET price = {price};')
"""


def get_point_links(vendor_id, level):
    q = db.i_request(f"SELECT url, brand FROM site_links WHERE vendor_id = {vendor_id} AND point = {level}")
    return q


def get_vendor_id(vendor):
    q = db.i_request(f"SELECT id FROM vendor WHERE vendor = '{vendor}'")
    if q:
        return q[0][0]
    else:
        return 0


def get_part_code_id(part_code):
    # q = db.i_request(f"WITH s as (SELECT id FROM partcodes "
    #                  f"WHERE code = '{part_code}'), i as "
    #                  f"(INSERT INTO partcodes (code) SELECT '{part_code}' "
    #                  f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    # if q:
    #     return q[0][0]
    # else:
    #     return 0
    q = db.i_request(f"SELECT id FROM partcodes WHERE code = '{part_code}'")
    if q:
        return q[0][0]
    else:
        return 0


def get_brand_id(brand):
    q = db.i_request(f"WITH s as (SELECT id FROM brands "
                     f"WHERE name = '{brand}'), i as "
                     f"(INSERT INTO brands (name) SELECT '{brand}' "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    if q:
        return q[0][0]
    else:
        return 0


def get_spr_modules_ru(module_ru):
    q = db.i_request(f"SELECT id FROM spr_modules WHERE name_ru = '{module_ru}'")
    if q:
        return q[0][0]
    else:
        return 0


def get_desc_partcodes():
    # return db.i_request(f"SELECT id, description FROM partcodes WHERE description = ''")
    return db.i_request(f"SELECT id, description FROM partcodes WHERE description is not NULL")


def update_desc_partcodes(id, desc):
    if desc:
        db.i_request(f"UPDATE partcodes SET description = '{desc}' WHERE id = {id}")
    else:
        db.i_request(f"UPDATE partcodes SET description = NULL WHERE id = {id}")


def get_model_id(model):
    q = db.i_request(f"SELECT id FROM models WHERE name = '{model}'")
    if q:
        return q[0][0]
    else:
        return 0


def get_module_id_details(part_id, model_id):
    q = db.i_request(f"SELECT module_id FROM details WHERE partcode_id = {part_id} AND model_id = {model_id}")
    if q:
        return q[0][0]
    else:
        return 0


def add_module(module):
    q = db.i_request(f"WITH s as (SELECT id FROM spr_modules "
                     f"WHERE name_ru = '{module}'), i as "
                     f"(INSERT INTO spr_modules (name_ru) SELECT '{module}' "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    if q:
        return q[0][0]
    else:
        return 0


def add_spr_details(name_ru, desc):
    if str(desc) != 'nan':
        q = db.i_request(f"WITH s as (SELECT id FROM spr_details "
                         f"WHERE name_ru = '{name_ru}' AND description = '{desc}' ), i as "
                         f"(INSERT INTO spr_details (name_ru, description) SELECT '{name_ru}', '{desc}' "
                         f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    else:
        q = db.i_request(f"WITH s as (SELECT id FROM spr_details "
                         f"WHERE name_ru = '{name_ru}' AND description = NULL ), i as "
                         f"(INSERT INTO spr_details (name_ru, description) SELECT '{name_ru}', NULL "
                         f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    if q:
        return q[0][0]
    else:
        return 0


def add_details(part_id, model_id, module_id):
    q = db.i_request(f"WITH s as (SELECT id FROM details "
                     f"WHERE partcode_id = {part_id} AND model_id = {model_id} AND module_id = {module_id} ), i as "
                     f"(INSERT INTO details (partcode_id, model_id, module_id) "
                     f"SELECT {part_id}, {model_id}, {module_id} "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    if q:
        return q[0][0]
    else:
        return 0


def update_module(module_id, param):
    db.i_request(f"UPDATE spr_modules SET name_ru = '{param}' WHERE id = {module_id}")


def get_details_spr_details(part_id, model_id, module_id):
    q = db.i_request(f"SELECT id FROM details WHERE partcode_id = {part_id} AND model_id = {model_id} "
                     f"AND module_id = {module_id} ")
    if q:
        return q[0][0]
    else:
        return 0


def update_spr_details(spr_detail_id, name_ru, desc):
    if str(desc) != 'nan':
        db.i_request(f"UPDATE spr_details SET name_ru = '{name_ru}', description = '{desc}' WHERE id = {spr_detail_id}")
    else:
        db.i_request(f"UPDATE spr_details SET name_ru = '{name_ru}', description = NULL WHERE id = {spr_detail_id}")


def update_partcode(brand_id, part_id, img, spr_detail_id):
    if str(img) != 'nan':
        db.i_request(
            f"UPDATE partcodes SET manufacturer = {brand_id}, images = '{img}', spr_detail_id = {spr_detail_id} "
            f"WHERE id = {part_id}")
    else:
        db.i_request(
            f"UPDATE partcodes SET manufacturer = {brand_id}, images = NULL, spr_detail_id = {spr_detail_id} "
            f"WHERE id = {part_id}")


def add_partcode(brand_id, partcode, img, spr_detail_id):
    if str(img) != 'nan':
        q = db.i_request(f"WITH s as (SELECT id FROM partcodes "
                         f"WHERE code = '{partcode}' AND manufacturer = {brand_id} AND spr_detail_id = {spr_detail_id}), i as "
                         f"(INSERT INTO partcodes (code, manufacturer, images) SELECT '{partcode}', {brand_id}, '{img}' "
                         f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    else:
        q = db.i_request(f"WITH s as (SELECT id FROM partcodes "
                         f"WHERE code = '{partcode}' AND manufacturer = {brand_id} ), i as "
                         f"(INSERT INTO partcodes (code, manufacturer, images) SELECT '{partcode}', {brand_id}, NULL "
                         f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    if q:
        return q[0][0]
    else:
        return 0


def get_spr_details(name_ru):
    q = db.i_request(f"SELECT id FROM spr_details WHERE name_ru = '{name_ru}'")
    if q:
        return q[0][0]
    else:
        return 0


def add_prices(price, vendor_id, part_id):
    db.i_request(f"WITH s as (SELECT id FROM prices "
                 f"WHERE price = {price} AND vendor_id = {vendor_id} AND partcode_id = {part_id} ), i as "
                 f"(INSERT INTO prices (price, vendor_id, partcode_id) "
                 f"SELECT {price}, {vendor_id}, {part_id} "
                 f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")


def get_spr_details_name(spr_detail_id):
    q = db.i_request(f"SELECT name_ru FROM spr_details WHERE id = {spr_detail_id}")
    return q


def get_modules_id(part_id, model_id):
    return db.i_request(f"SELECT module_id FROM details WHERE model_id = {model_id} AND partcode_id = {part_id}")


def get_all_partcode_spr_details_is_null():
    return db.i_request(f"SELECT id FROM partcodes WHERE spr_detail_id IS NULL")


def get_spr_detail_id_in_details(part_id):
    q = db.i_request(f"SELECT model_id, spr_detail_id FROM details WHERE partcode_id = {part_id} LIMIT 1 OFFSET 0")
    if q:
        return q
    else:
        return 0


def get_brand_id_in_models(model_id):
    q = db.i_request(f"SELECT brand_id FROM models WHERE id = {model_id}")
    if q:
        return q[0][0]
    else:
        return 0


def linked_partcode(part_id, brand_id, spr_detail_id):
    db.i_request(f"UPDATE partcodes SET manufacturer = {brand_id}, spr_detail_id = {spr_detail_id} "
                 f"WHERE id = {part_id}")


def get_ids(param):
    return db.i_request(f"SELECT id FROM {param}")


def add_partcode_article(part_id, article_code):
    db.i_request(f"UPDATE partcodes SET article_code = '{article_code}' WHERE id = {part_id}")


def get_detail_id_is_not_partcode():
    return db.i_request(f"SELECT id, model_id, spr_detail_id FROM details "
                        f"WHERE partcode_id IS NULL AND module_id IS NOT NULL")


def get_max_article_code():
    q = db.i_request(f"SELECT article_code FROM partcodes ORDER BY article_code DESC")
    if q:
        return q[0][0]
    else:
        return 0


def add_partcode_article_manufacture_spr_details(article_code, brand_id, spr_detail_id):
    q = db.i_request(f"WITH s as (SELECT id FROM partcodes "
                     f"WHERE article_code = '{article_code}' AND manufacturer = {brand_id} AND spr_detail_id = {spr_detail_id}), i as "
                     f"(INSERT INTO partcodes (code, article_code, manufacturer, spr_detail_id) "
                     f"SELECT '{article_code}', '{article_code}', {brand_id}, {spr_detail_id} "
                     f"WHERE NOT EXISTS (SELECT 1 FROM s) RETURNING id) SELECT id FROM i UNION ALL SELECT id FROM s")
    if q:
        return q[0][0]
    else:
        return 0


def update_details_partcode(detail_id, part_id):
    db.i_request(f"UPDATE details SET partcode_id = {part_id} WHERE id = {detail_id}")
