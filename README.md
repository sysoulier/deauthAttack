# ddos_wireless
Projet de création d'une attaque ddos sur un réseau sans fil

## Phase de reconnaissance :
#### Passer l'interface wifi de la machine en mode monitor  

1 - Verifier interfaces Wifi-disponibles :
```
iwconfig
```

2 - Arreter l'interface Wifi :
```
sudo ifconfig wlan0 down
```

3 - Passer en mode monitor :
```
sudo airmon-ng start wlan0
```

4 - Capturer les informations des réseaux Wifi :
```
sudo airodump-ng wlan0mon
```

#### Repasser en mode managed :

1 - Arreter le mode monitor :
```
sudo airmon-ng stop wlan0mon
```

2 - Reactiver l'interface Wifi :
```
sudo ifconfig wlan0 up
```
