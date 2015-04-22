#!/usr/local/bin/python2.7

import re
import subprocess as sub

#p = sub.Popen('/sbin/mdadm --detail /dev/md0',stdout=sub.PIPE,stderr=sub.PIPE)
#output, errors = p.communicate()

md0 = sub.check_output(["/sbin/mdadm", "--detail", "/dev/md0"])
aActive      = int(re.findall(r'Active.*: (\d*)', md0)[0])
aWorking     = int(re.findall(r'Working.*: (\d*)', md0)[0])
aRaidDevices = int(re.findall(r'Raid Devices.*: (\d*)', md0)[0])
aSize        = float(re.findall(r'Array Size.*: (\d*)', md0)[0])
aDegraded    = aActive < aRaidDevices

md1 = sub.check_output(["/sbin/mdadm", "--detail", "/dev/md1"])
bActive      = int(re.findall(r'Active.*: (\d*)', md1)[0])
bWorking     = int(re.findall(r'Working.*: (\d*)', md1)[0])
bRaidDevices = int(re.findall(r'Raid Devices.*: (\d*)', md1)[0])
bSize        = float(re.findall(r'Array Size.*: (\d*)', md1)[0])
bDegraded    = bActive < bRaidDevices

tSize = aSize + bSize
rebuiltSize = 0
rSize = 0
aRebuilding = False
bRebuilding = False

msgStr = "RAID1 : Unknown state."

if( ( aWorking != 2 ) and ( bWorking != 2 ) ):
    msgStr = "RAID1 :  Mirror offline     "
else:
    aState   = re.findall(r'State.*: (\w*)', md0)[0]
    bState   = re.findall(r'State.*: (\w*)', md1)[0]

    if aState == 'resyncing' or aState == 'recovering':
        aRebuilding = True

    if bState == 'resyncing' or bState == 'recovering':
        bRebuilding = True

    Rebuilding  = ( aRebuilding ) or ( bRebuilding );

    if not Rebuilding:
        if( ( aActive == 2) and ( bActive == 2 ) ):
            msgStr = "RAID1 :  Operational        "
        else:
            pass

    else:
        if aRebuilding:
            a = int(re.findall(r'Rebuild Status.*: (\d*)', md0)[0])
            aCpc  = a/100
            rSize = aCpc * aSize
        elif not aDegraded:
            rebuiltSize += aSize

        if bRebuilding:
            b = int(re.findall(r'Rebuild Status.*: (\d*)', md1)[0])
            bCpc  = b/100
            rSize = bCpc * aSize

        elif not bDegraded:
            rebuiltSize += bSize

        pComplete = ((rSize + rebuiltSize) / tSize) * 100
        msgStr    = "RAID1 :  Rebuilding " + str(pComplete*100)

print msgStr
#return (statusByte, msgStr)
