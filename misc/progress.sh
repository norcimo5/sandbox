#!/bin/sh
(
echo "10"; sleep 1
echo "# Configuring Router Intefaces" ; sleep 1
echo "20" ; sleep 1
echo "# Backing Up Running Config" ; sleep 1
echo "50" ; sleep 1
echo "# Copying New Config To Router" ; sleep 1
echo "75" ; sleep 1
echo "# Installing New Config" ; sleep 1
echo "100" ; sleep 1
echo "# Update Complete" ; sleep 1
) |
zenity --progress \
  --title="CISCO 819 AutoConfig" \
  --text="Initializing Router Connection..." \
  --percentage=0 \
  --width=500 \

if [ "$?" = -1 ] ; then
        zenity --error \
          --text="Update canceled."
fi
