#!/usr/bin/python

import fcntl
import glob
import os
import struct
import sys
import termios

from textwrap import TextWrapper

#
# Pretty-print the output.  The first bit of guck gets us the terminal size.
# When run from within ant, stdin, stdout, and stderr aren't available for
# termios querying, so we wrap it all in try/except and provide a usable
# default.
#
(rows, columns) = (0, 0)

try:
    (rows, columns) = struct.unpack('hh',
                                fcntl.ioctl(sys.stdout,
                                            termios.TIOCGWINSZ,
                                            '1234'))
except IOError:
    columns = 80

text_wrap = TextWrapper(width=columns, subsequent_indent='    ')

file_list_files = glob.glob(os.path.join('*', 'files.list'))
targets_file    = os.path.join(os.pardir, 'SPECS', 'Targets')

rpm_file_dict = {}

for f in file_list_files:
    key = 'TGI-config-' + os.path.dirname(f)
    fh  = file(f, "r")

    rpm_file_dict[key] = set()

    for line in fh.readlines():
        #
        # Some sorry-a**ed editors (or their users) leave blank lines at the
        # end, so deal with that.
        #
        if len(line.strip()) == 0:
            continue

        filename = line.split()[-1]

        rpm_file_dict[key].add(filename)

    fh.close()

#
# For now, we only care about TGI-config-* rpms.  We'll get around to more
# stringent conflict checking later.
#
rpm_file_dict['dgnc']                     = set()
rpm_file_dict['sbs_a429pci']              = set()
rpm_file_dict['TGI-TFDOA-hwConfig']       = set()
rpm_file_dict['TGI-tews-2.6.18']          = set()
rpm_file_dict['TGI-rmd-gate']             = set()
rpm_file_dict['TGI-picoceptor-utility']   = set()

#
# This alleviates the issue for doc rpms.  The docs have the same names, but
# the contents are different.  Only one docs rpm will be installed by
# install-node.
#
rpm_file_dict['TGI-CP2-v1-dpu-doc']       = set()
rpm_file_dict['TGI-V3-DPU-doc']           = set()
rpm_file_dict['TGI-command-doc']          = set()
rpm_file_dict['TGI-firefly-doc']          = set()
rpm_file_dict['TGI-firefly-gpsd-doc']     = set()
rpm_file_dict['TGI-firefly-payload-doc']  = set()
rpm_file_dict['TGI-gate-doc']             = set()
rpm_file_dict['TGI-hagate-doc']           = set()
rpm_file_dict['TGI-SB1-systel-doc']       = set()
rpm_file_dict['TGI-SB1-refresh-doc']      = set()
rpm_file_dict['TGI-SBD1-systel-doc']      = set()
rpm_file_dict['TGI-SC1-systel-doc']       = set()
rpm_file_dict['TGI-SCD1-systel-doc']      = set()
rpm_file_dict['TGI-sentry-spu-doc']       = set()
rpm_file_dict['TGI-single-host-gate-doc'] = set()
rpm_file_dict['TGI-SR1-systel-doc']       = set()
rpm_file_dict['TGI-SR3-systel-doc']       = set()
rpm_file_dict['TGI-DRT-1301-doc']         = set()
rpm_file_dict['TGI-DRT-4411-doc']         = set()
rpm_file_dict['TGI-DRT-C2-doc']           = set()
rpm_file_dict['TGI-DRT-C3-doc']           = set()
rpm_file_dict['TGI-DRT-M2-doc']           = set()
rpm_file_dict['TGI-DRT-E3-doc']           = set()
rpm_file_dict['TGI-DRT-F2-doc']           = set()
rpm_file_dict['TGI-DRT-F3-doc']           = set()
rpm_file_dict['TGI-DRT-P2-doc']           = set()
rpm_file_dict['TGI-DRT-R2-doc']           = set()
rpm_file_dict['TGI-TIK-doc']              = set()
rpm_file_dict['TGI-DRT-CB2-doc']          = set()
rpm_file_dict['TGI-xgate-doc']            = set()

#
# This one is special.  It has no files; it's just scriptlets.
#
rpm_file_dict['TGI-config-post'] = set()

#
# We only care about checking RPMs that get installed together on a given
# target.
#
# The format of the Targets file is
#
# target-name,IMA1 [IMA2 ...],config-rpm1 [config-rpm2 ...]
#
targets_fh = file(targets_file, "r")
targets    = {}

for line in targets_fh.readlines():
    if line.startswith('#') or len(line.strip()) == 0:
        continue

    (target_name, imalist, rpmlist) = line.split(',')

    targets[target_name] = rpmlist.split()

targets_fh.close()

found_conflict = False

for t in targets:
    #
    # This loop is N^2 over the list of config RPMs installed on a target, but
    # it's so easy to express this way, and that list is so short that it
    # doesn't pay to obfusc^h^h^h^h^h^hoptimize it.
    #
    intersecting_rpms = set()

    for test_rpm in targets[t]:

        for rpm in targets[t]:
            if test_rpm == rpm:
                continue

            #
            # De-dup.  If we've already listed this pair one way, we don't need
            # to list it again with the operands reversed.
            #
            if rpm in intersecting_rpms:
                continue
            #else:
            #    print "%s, %s" % (rpm, intersecting_rpms)

            common_files = rpm_file_dict[test_rpm] & rpm_file_dict[rpm]

            if len(common_files) > 0:
                intersecting_rpms.add(test_rpm)

                found_conflict = True

                print text_wrap.fill("target '%s': rpms '%s' and '%s' have the following files in common:" % (t, test_rpm, rpm))

                for f in common_files:
                    print "\t", f

                print ''

if found_conflict:
    sys.exit(1)

#
# vim:ft=python
#
