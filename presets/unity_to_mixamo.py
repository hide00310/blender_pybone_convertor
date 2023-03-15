"""
MIT License

Copyright (c) 2022 hide00310

This script logic is based on the Mina Pêcheux's script:
    https://github.com/MinaPecheux/BlenderPlugins/blob/master/Rigging/MixamoRigRenamer.py

Copyright (c) 2022 Mina Pêcheux

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
