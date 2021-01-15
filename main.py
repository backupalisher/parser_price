import re
# from profit_msk.html_parser import parse_prifit_msk
# from profit_msk import profit_msk
# from utils import fix_desc_partcodes
from profit_msk.db_parser import db_parser
# from profit_msk import fix_files_partcodes


def main():
    # parse_prifit_msk.model_parse()
    # profit_msk.start()
    # fix_desc_partcodes.get_id_partcodes()
    # fix_files_partcodes.start()
    db_parser.start()


if __name__ == '__main__':
    main()
