from utils import db_utils


def get_id_partcodes():
    ids = db_utils.get_desc_partcodes()
    max_len = len(ids)
    for n, i in enumerate(ids):
        # print(i)
        desc = i[1]
        desc = desc.split(';')
        desc = [x for x in desc if x != '']
        new_desc = list(set(desc))
        res = ''
        for j in new_desc:
            res += j + ';'
        print(max_len, n, res)
        db_utils.update_desc_partcodes(i[0], res)
