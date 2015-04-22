#!/usr/bin/env python2.7

import os
import re

firmwareStr = "02.06.01-|B63"
regex       = re.findall(r'^(\d*)\.(\d*)\.(\d*)-\|B(\d*)', firmwareStr)[0]

print regex
