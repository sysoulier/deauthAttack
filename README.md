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
5 - Information spécifique sur un réseau ( sortie dans output/client )
'''
sudo airodump-ng --bssid <BSSID> -c <channel> -w output/client wlan0mon
'''
#### Repasser en mode managed :

1 - Arreter le mode monitor :
```
sudo airmon-ng stop wlan0mon
```

2 - Reactiver l'interface Wifi :
```
sudo ifconfig wlan0 up
```

## Phase de préparation
#### Recuperation des adresses MAC

1 - Récuperation des adresses MAC des machines connectées au réseau : 
```
awk -F ',' {'print $1'} output/client-01.csv | sed '1,5d' > client.txt
```
2 - Donner les droits au fichier
```
chmod 700 client.txt
```

#### Installation outils
Installation de l'outils de traduction MAC -> Marque (OUI)
```
git clone https://github.com/silverwind/oui.git
sudo apt install npm
npm i -g oui
```

## Phase d'attaque
Il faut penser à recuperer le bssid à attaque avec son channel

```
sudo python3 deauth.py
```

