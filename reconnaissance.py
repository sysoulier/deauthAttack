import subprocess

# Exécute la commande wpa_cli pour obtenir la liste des réseaux Wi-Fi disponibles
output = subprocess.check_output(["sudo", "wpa_cli", "-i", "en0", "list_networks"])

# Convertit la sortie en une chaîne de caractères et la divise en lignes
output = output.decode("utf-8").split("\n")

# Ignore la première ligne (en-tête)
output = output[1:]

# Parcourez les lignes pour obtenir les informations sur les réseaux
for line in output:
    fields = line.split()
    if len(fields) >= 4:
        network_id, ssid, bssid, flags = fields[:4]
        print(f"Network ID: {network_id}, SSID: {ssid}, BSSID: {bssid}, Flags: {flags}")