#! /usr/bin/env python3

import os
import argparse

from report import report 
from create_db import create_db
from to_db import update_db
from config import defaults

def run():
    main_parser = argparse.ArgumentParser()
    
    subparser = main_parser.add_subparsers()
    #subparser.required=True
    #subparser.dest='createdb'
    
    # db parsers
    create_db_parser = subparser.add_parser('createdb',
        help='command to create new database')
    create_db_parser.add_argument('--dbname',
        default=defaults['DATABASE_NAME'], help='specify name of database')
    create_db_parser.set_defaults(func=create_db)

    update_db_parser = subparser.add_parser('updatedb',
        help='''command to ingest text files, tokenize and
        insert processed data into database''')
    update_db_parser.add_argument('--path',
        help='path to directory contaning docs to process')
    update_db_parser.add_argument('--dbname',
        default=defaults['DATABASE_NAME'], help='name of databse')
    update_db_parser.set_defaults(func=update_db)

    
    # report parser
    report_parser = subparser.add_parser('report',
        help='generate report of most(least) common words(lemmas)')
    report_parser.add_argument('--filename', 
        default=defaults['REPORT_NAME'], help='filename to save to')
    report_parser.add_argument('--documents', nargs='+',
        help='document names to include in report. all included by default')
    report_parser.add_argument('--limit', type=int, default=10, 
        help='number of most(least) common words(lemmas) to include in report')
    report_parser.add_argument(
        '--most', default=True, action='store_false',
        help='include argument if report least common. reports most common by default')
    report_parser.add_argument('--dbname',
        default=defaults['DATABASE_NAME'], help='name of database')
    report_parser.add_argument('--display_format', 
        default='html', help='export format')
    report_parser.add_argument('--lemmas', default=False, action='store_true',
        help='include argument if report most(least) common lemmas instead of words')
    report_parser.set_defaults(func=report)
    
    
    args = main_parser.parse_args()
    vargs = vars(args)
    if len(vargs) == 0:
        return
    vargs = {k:v for k,v in vargs.items() if k!='func'}

    args.func(**vargs)

    

if __name__ == '__main__':
    run()
