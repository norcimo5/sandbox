OUTPUT=$(zenity --forms --title="Add Friend" --text="Enter Multicast address" --separator="," --add-entry="IP address" --add-entry="PORT")
accepted=$?
if ((accepted != 0)); then
    echo "something went wrong"
        exit 1
        fi

        ip=$(awk -F, '{print $1}' <<<$OUTPUT)
        port=$(awk -F, '{print $2}' <<<$OUTPUT)

        echo $ip
        echo $port
