# Deauth Attack Dos
Projet de création d'une attaque dos sur un réseau sans fil via l'utilisation de trame Deauth.

Outils développé en utilisant python et scapy.

## Installation :

```
sudo apt-get install aircrack-ng
sudo pip3 install -r requirements.txt
chmod +x script/*
git clone https://github.com/silverwind/oui.git
sudo apt install npm
npm i -g oui
```

## Phase de reconnaissance :  

#### Trouver un un reseau :

Avec une interface en mode monitor affichez les bssid des réseaux à proximités.
```
sudo airodump-ng <interface_monitor>
```

## Phase d'attaque
Il faudra connaitre le bssid et le channel du reseau victime.

Assurez vous d'utiliser une interface réseau sans fil qui pourra passer en mode monitor.

```
sudo python3 deauth.py
```

