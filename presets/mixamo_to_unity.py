import re
import sys
import os
module_dir = os.path.dirname(__file__)
if module_dir not in sys.path:
    sys.path.append(module_dir)
from _unity_mixamo_util import mix_to_unity_dict, mixamo_prefix


def rename(context, name):
    for k, v in mix_to_unity_dict.items():
        new_name = re.sub(k, v, name)
        if new_name != name:
            name = new_name
            break
    name = name[len(mixamo_prefix):]
    if 'Left' in name:
        name = name[4:] + '.L'
    elif 'Right' in name:
        name = name[5:] + '.R'
    return name
