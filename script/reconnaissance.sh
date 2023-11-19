#!/bin/bash

if [[ -e "/sys/class/net/$3" ]]
then
	airodump-ng --bssid $1 -c $2 -w output/client $3 & sleep 15 ; kill $!
else
	echo "$3 n'existe pas"
fi

