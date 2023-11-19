#!/bin/bash

interface=$1

if ! iw dev "$interface" info &>/dev/null
then
	echo "L'interface $interface n'existe pas "
	exit 1
fi

iwconfig_output=$(iwconfig "$interface" 2>/dev/null)

if [[ $iwconfig_output == *Mode:Monitor* ]]
then
	echo "L'interface $interface est en mode monitor"
else 
	echo "L'interface $interface va passer en mode  monitor"
	airmon-ng start $interface
	echo "L'interface $interface est en mode monitor"
fi
