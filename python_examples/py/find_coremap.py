#!/usr/bin/env python2.7

import os

core0_temp = 0
core2_temp = 0
for root, dirs, files in os.walk("/sys"):
    for file in files:
        if file.endswith("temp1_input"):
            if root.endswith("coretemp.0"):
                with open(os.path.join(root, file), 'r') as f:
                    core0_temp = int(f.readline()) / 1000
            elif root.endswith("coretemp.1"):
                with open(os.path.join(root, file), 'r') as f:
                    core2_temp = int(f.readline()) / 1000

print core0_temp
print core2_temp
