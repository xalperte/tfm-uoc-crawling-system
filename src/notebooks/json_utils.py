# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
import gzip
import json


def write_to_gzip_file(gzip_filename, data):

    json_str = json.dumps(data) + "\n"  # 2. string (i.e. JSON)
    json_bytes = json_str.encode('utf-8')  # 3. bytes (i.e. UTF-8)

    with gzip.GzipFile(gzip_filename, 'w') as f_out:  # 4. gzip
        f_out.write(json_bytes)


def load_from_gzip_file(gzip_filename):
    with gzip.GzipFile(gzip_filename, 'r') as fin:  # 4. gzip
        json_bytes = fin.read()  # 3. bytes (i.e. UTF-8)

    json_str = json_bytes.decode('utf-8')  # 2. string (i.e. JSON)
    return json.loads(json_str)  # 1. data
