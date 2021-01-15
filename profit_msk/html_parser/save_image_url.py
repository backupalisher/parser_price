import os

import requests
import shutil


def save_image_url(url, path, fn):
    options_list = []
    if url:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(os.path.join(path, f'{fn}.jpg'), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            options_list.append(['img_path', os.path.join(path, f'{fn}.jpg')])
    return options_list
