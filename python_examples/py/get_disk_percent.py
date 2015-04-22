#!/usr/bin/env python2.7

import subprocess
import re

def get_disk_usage():
    df = subprocess.Popen(["/bin/df", "/"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = output.split("\n")[1].split()

    p = 0
    try:
        p = int(re.findall(r'(\d+)%' , percent)[0])
    except:
        pass

    return p

print get_disk_usage()
