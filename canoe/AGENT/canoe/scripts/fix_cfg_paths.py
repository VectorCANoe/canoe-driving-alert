import os
import re

cfg = 'cfg/CAN_500kBaud_1ch_split.cfg'
with open(cfg, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

before = sum(1 for l in lines if '?????' in l or '\ufffd' in l)
target_root = os.path.join(os.path.expanduser('~'), 'CANoe-IVI-OTA')
corrupted_pattern = r'C:\\Users\\[^\\]*\\?CANoe-IVI-OTA'

fixed = []
for line in lines:
    if 'CANoe-IVI-OTA' in line and ('?????' in line or '\ufffd' in line):
        # Replace corrupted username segment after Users\.
        line = re.sub(corrupted_pattern, lambda _: target_root, line)
    fixed.append(line)

after = sum(1 for l in fixed if '?????' in l or '\ufffd' in l)
print(f'Corrupted path lines: {before} -> {after}')

with open(cfg, 'w', encoding='utf-8') as f:
    f.writelines(fixed)

print('Done')
