import re

cfg = 'cfg/CAN_500kBaud_1ch_split.cfg'
with open(cfg, encoding='utf-8', errors='replace') as f:
    content = f.read()

# 1. mojibake cbf paths -> relative paths
def fix_cbf(line):
    if '\ufffd' in line and '.cbf' in line:
        m = re.search(r'src.capl.(.+\.cbf)', line.replace('\ufffd', '?'))
        if m:
            return '..' + chr(92) + 'src' + chr(92) + 'capl' + chr(92) + m.group(1) + '\n'
    return line

lines = content.splitlines(keepends=True)
lines = [fix_cbf(l) for l in lines]
content = ''.join(lines)

# 2. ETH_SW network blank -> chassis_can
content = content.replace('ETH_SW\n\n5\n', 'ETH_SW\nchassis_can\n5\n')

bad = content.count('\ufffd')
eth_ok = 'ETH_SW\nchassis_can' in content

with open(cfg, 'w', encoding='utf-8') as f:
    f.write(content)

print("mojibake remaining: " + str(bad))
print("ETH_SW->chassis_can: " + str(eth_ok))
