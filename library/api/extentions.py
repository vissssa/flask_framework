import os
import re
import sys
from os.path import join, splitext, dirname, abspath
from pathlib import Path

import yaml

from library.api.parse import TParse
from library.api.validation import Validation

"""
由于我们的启动方式
python -m apps.public.run
所以由此方式来获取服务名称以及对应路径
"""
current_path = Path(f"apps/{re.findall('apps/(.+?)/run', sys.argv[0])[0]}")
yml_json = {}

while True:
    try:
        validate_yml_path = join(current_path, 'validations')
        for fi in os.listdir(validate_yml_path):
            if splitext(fi)[-1] != '.yml':
                continue
            with open(join(validate_yml_path, fi), 'rb') as f:
                yml_json.update(yaml.safe_load(f.read()))
    except FileNotFoundError:
        current_path = dirname(abspath(__name__))
    except Exception as e:
        print(e)
        break
    else:
        break

v = Validation(yml_json)
validation = v.validation

p = TParse(yml_json)
parse_list_args = p.parse_list_args
parse_list_args2 = p.parse_list_args2
parse_json_form = p.parse_json_form
parse_json_formdict = p.parse_json_formdict
parse_pwd = p.parse_pwd
