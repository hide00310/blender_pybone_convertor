import re
import sys
import os
module_dir = os.path.dirname(__file__)
if module_dir not in sys.path:
    sys.path.append(module_dir)
from _unity_rigify_util import unity_to_rigify_dict

def rename(context, name):
    name = re.sub(r'\s', '', name)
    for k, v in unity_to_rigify_dict.items():
        new_name = re.sub(k, v, name)
        if new_name != name:
            name = new_name
            break
    name = f'{name[0].lower()}{name[1:]}'
    return name
