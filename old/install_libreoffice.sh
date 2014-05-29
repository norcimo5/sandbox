#!/bin/bash
#set -o xtrace
## For 64-Bit OS ##

#sudo yum remove openoffice.org* libreoffice.org*
cd /var/tmp
#tar -xvf LibO_3.6.2_Linux_x86-64_install-rpm_en-US.tar.gz

cd LibO_3.6.2.2_Linux_x86-64_install-rpm_en-US/RPMS/
sudo rpm -Uvh *.rpm
sudo rpm -Uvh desktop-integration/libreoffice3.6-freedesktop-menus-3.6*.noarch.rpm
