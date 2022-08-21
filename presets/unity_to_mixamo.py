import re
import sys
import os
module_dir = os.path.dirname(__file__)
if module_dir not in sys.path:
    sys.path.append(module_dir)
from _unity_mixamo_util import unity_to_mix_dict, mixamo_prefix


def rename(context, name):
    name = re.sub(r'\s', '', name)
    for k, v in unity_to_mix_dict.items():
        new_name = re.sub(k, v, name)
        if new_name != name:
            name = new_name
            break
    if name.endswith('.L'):
        name = 'Left' + name[:-2]
    elif name.endswith('.R'):
        name = 'Right' + name[:-2]
    name = mixamo_prefix + name
    return name
