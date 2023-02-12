#!/usr/bin/python3

import re
import json
import argparse
import os

def read_file(file_path):
    with open(file_path,'rb') as f:
        file_contents = json.load(f)
        return file_contents

def dict_compare(d1, d2, previous_date, now_date):
    diff = ()
    for k in d1:
        print(k + ': ')
        # 在 1中而不在2中 -> successful
        print('Old disappered packages since previous build(%s):' % previous_date)
        diff = set(re.split(',', d1[k])) - set(re.split(',', d2[k]))
        if bool(diff):
            print(diff)
        else:
            print("No change")
        # 在2中而不在1中 -> failed
        print('New added packages at last build(%s):' % now_date)
        diff = set(re.split(',', d2[k])) - set(re.split(',', d1[k]))
        if bool(diff):
            print(diff)
        else:
            print("No change")

        print("\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyst buildd status")
    parser.add_argument('--old', '-o', help='previous build json file', required=True)
    parser.add_argument('--new', '-n', help='now build json file', required=True)
    args = parser.parse_args()
    try:
        f1_path = args.old
        f2_path = args.new
    except Exception as e:
        print(e)

    previous_date = os.path.splitext(f1_path)[0].split('/')[1]
    now_date = os.path.splitext(f2_path)[0].split('/')[1]
    d1 = read_file(f1_path)
    d2 = read_file(f2_path)
    
    dict_compare(d1, d2, previous_date, now_date)
