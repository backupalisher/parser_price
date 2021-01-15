import re


def check_http(link, l_link):
    try:
        if re.search(r'.{4}', link)[0] != 'http':
            link = re.sub(r'/.*$', '', l_link) + link

        return link
    except:
        pass
