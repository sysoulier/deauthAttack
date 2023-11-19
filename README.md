# Deauth Attack Dos
Projet de création d'une attaque dos sur un réseau sans fil via l'utilisation de trame Deauth

## Installation :

```
sudo apt-get install aircrack-ng
pip install -r requirements.txt
chmod +x script/*
git clone https://github.com/silverwind/oui.git
sudo apt install npm
npm i -g oui
```

## Phase de reconnaissance :  

#### Trouver un un reseau :

Avec une interface en mode monitor afficher les bssid des réseaux à proximiter
```
sudo airodump-ng <interface_monitor>
```

## Phase d'attaque
Il faudra connaitre le bssid et le channel du reseau victime

```
sudo python3 deauth.py
```

