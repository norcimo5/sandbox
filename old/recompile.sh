#!/bin/bash
#set -o xtrace

export RHEL_DEBUG=rhel_5_i386/debug
cd /build/4.0-tng

if [[ -e /var/tmp/NOT_IN_JAIL ]]; then
    zenity --info --text "ERROR : NOT IN JAIL !!! :-("
    exit 1;
fi

echo [ DELETING $RHEL_DEBUG ]
rm -rf $RHEL_DEBUG
scons $RHEL_DEBUG
if [[ $? -eq 0 ]]; then
    zenity --info --text "SCONS DEBUG BUILD COMPLETED SUCCESSFULY! :-)"
else
    zenity --info --text "ERROR : SCONS DEBUG BUILD BLEW UP! :-("
fi

cd -

exit 0;
