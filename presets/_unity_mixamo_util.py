_unity_to_mix_dict = {
    'Chest': 'Spine1',
    'UpperChest': 'Spine2',
    'LowerArm': 'ForeArm',
    'UpperArm': 'Arm',
    'UpperLeg': 'UpLeg',
    'LowerLeg': 'Leg',
    'Toes': 'ToeBase',
}
for i, name in enumerate(['Proximal', 'Intermediate', 'Distal']):
    _unity_to_mix_dict['Little' + name] = f'HandPinky{i+1}'
# $ is regex mark. e.g. "ThumbProximal" to "HandThumb1".
for i, name in enumerate(['Proximal', 'Intermediate', 'Distal']):
    _unity_to_mix_dict['$' + name] = f'Hand${i+1}'

unity_to_mix_dict = {}
for k, v in _unity_to_mix_dict.items():
    unity_to_mix_dict[k.replace('$', r'(\w+)')] = v.replace('$', r'\g<1>')

mix_to_unity_dict = {}
for k, v in _unity_to_mix_dict.items():
    mix_to_unity_dict[v.replace('$', r'(\w+)')] = k.replace('$', r'\g<1>')

mixamo_prefix = 'mixamorig:'
