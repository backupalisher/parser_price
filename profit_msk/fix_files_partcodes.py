import re
import os

import pandas


def start():
    for root, dirnames, filenames in os.walk(os.path.join("profit_msk", "parse")):
        for file in filenames:
            if file.endswith("_parts.csv"):
                print(file)
                fn = os.path.join(root, file)
                fix_file(fn, file)


def fix_file(file_path, file_name):
    with open(file_path, encoding='utf-8') as f:
        d_text = False
        old_line = ''

        for line in f:
            if re.search(r'\u0020\(Включает:([^<]*)\)', line):
                nt = re.search(r'\u0020\(Включает:([^<]*)\)', line).group(0)
                nt = re.sub(';', ',', nt)
                line = re.sub(r'\u0020\(Включает:([^<]*)\)', nt, line)

            if not d_text:
                if re.search(r'\)";"', line):
                    d_text = True
                    line = re.sub(r'\)";".*', ');', line)
            elif d_text:
                if re.search(r'\)";', line):
                    d_text = False
                    line = re.sub(r'\)";', ');', line)
                else:
                    continue

            line = re.sub(r'\u0020\(Включает:', r';(Включает:', line)
            line = re.sub(r';"', ';', line)

            row_count = line.split(';')
            if len(row_count) == 8:
                line = re.sub(r'\n', '', line)
                # print(line, 'ok')
                line = copy_name_desc(line, file_name)
                # print(len(line), line)
            elif not d_text:
                line = re.sub(r'\n', '|||', line)
                old_line += line
                old_line = re.sub(r'\|\|\|', f'\n', old_line)
                row_count = old_line.split(';')
                if len(row_count) == 8:
                    # print(old_line)
                    line = re.sub(r'\n', '', old_line)
                    old_line = ''
                    line = copy_name_desc(line, file_name)
                    # print(len(line), line)


def copy_name_desc(line, file_name):
    line = line.split(';')
    if re.search(f'\u0020\([^)]*\)|, в сборе', line[3]):
        desc = None
        if re.search(f'\u0020\([^)]*\)$', line[3]):
            desc = re.search(f'\([^)]*\)', line[3]).group(0)
        elif re.search(f'(, в сборе)\w|(, в сборе)\u0020', line[3]):
            n = re.search(f'.*, в сборе', line[3]).group(0)
            desc = re.sub(f'{n}', '', line[3]).strip()
        elif re.search(f'\u0020\(.*', line[3]):
            desc = re.search(f'\u0020\(.*', line[3]).group(0)
        if desc:
            line[3] = line[3].replace(desc, '').replace('"', '').strip()
            if not re.search(r'\)\u0020|\)\w', desc.strip()):
                desc = re.sub(r'^\(|\)$|\n$', '', desc).replace('"', '').strip()
            desc.replace('"', '').strip()
            desc = re.sub(rf'\)\w|\)\u0020{1,}', '\r\n', desc)
            if line[4]:
                od = line[4].replace('"', '')
                line[4] = f'{desc}\n{od}'
            else:
                line[4] = desc

    t_path = os.path.join('profit_msk', 'parse2')
    base_path = os.path.join(t_path, re.sub(rf'\s.*', '', file_name))
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    df = pandas.DataFrame([line])
    df.to_csv(os.path.join(base_path, file_name),
              index=False, mode='a', encoding='utf-8', header=False, sep=";")
    return line
