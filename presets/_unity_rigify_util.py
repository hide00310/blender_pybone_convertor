_convert_dict = {
    'Head': 'spine.006',
    'Neck': 'spine.004',
    'UpperChest.001': 'spine.003',
    '^UpperChest$': 'spine.002',
    '^Chest$': 'spine.001',
    'Hips': '^spine$',
    'LowerArm': 'forearm',
    'UpperArm': 'upper_arm',
    'UpperLeg': 'thigh',
    'LowerLeg': 'shin',
    'Toes': 'toe',
}
for i, name in enumerate(['Proximal', 'Intermediate', 'Distal']):
    _convert_dict['Thumb' + name] = f'thumb.{i+1:02}'
for i, name in enumerate(['Index', 'Middle', 'Ring', 'Little']):
    _convert_dict[f'{name}Proximal'] = f'palm.{i+1:02}'
for i, name in enumerate(['Index', 'Middle', 'Ring']):
    for j, name2 in enumerate(['Intermediate', 'Distal']):
        _convert_dict[f'{name}{name2}'] = f'f_{name.lower()}.{j+1:02}'
for i, name in enumerate(['Intermediate', 'Distal']):
    _convert_dict[f'{name}Little'] = f'f_pinky.{i+1:02}'

unity_to_rigify_dict = {}
for k, v in _convert_dict.items():
    unity_to_rigify_dict[k] = v.replace('^', '').replace('$', '')

rigify_to_unity_dict = {}
for k, v in _convert_dict.items():
    rigify_to_unity_dict[v] = k.replace('^', '').replace('$', '')
