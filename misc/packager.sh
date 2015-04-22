#!/bin/bash
#set -o xtrace
rsync -rlpgoD --exclude client /h/ShutdownManager/ /tmp/h/ShutdownManager
cd /tmp
#generate the post_install.sh
tee /tmp/h/post_install.sh << ! &> /dev/null
#!/bin/bash
echo "[ INSTALLING SHUTDOWN MANAGER ]"

echo "[            DONE             ]"
!

makeself --gzip h/ sm_snare_installer.run "Shutdown Manager Installer for Snare" ./post_install.sh
