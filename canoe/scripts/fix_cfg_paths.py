import re

cfg = 'cfg/CAN_500kBaud_1ch_split.cfg'
with open(cfg, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

before = sum(1 for l in lines if '?????' in l or '\ufffd' in l)
fixed = []
for line in lines:
    if 'CANoe-IVI-OTA' in line and ('?????' in line or '\ufffd' in line):
        # Users\ 다음 깨진 username 부분을 이준영으로 교체 (백슬래시 없는 경우도 처리)
        line = re.sub(r'C:\\Users\\[^\\]*\\?CANoe-IVI-OTA', r'C:\\Users\\이준영\\CANoe-IVI-OTA', line)
    fixed.append(line)

after = sum(1 for l in fixed if '?????' in l or '\ufffd' in l)
print(f'깨진 경로 라인: {before} -> {after}')

with open(cfg, 'w', encoding='utf-8') as f:
    f.writelines(fixed)

print('완료')
