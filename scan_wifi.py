import pywifi

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]  # Sélectionnez la première interface Wi-Fi

print(iface)

'''
scan_results = iface.scan_results()
for result in scan_results:
    bssid = result.bssid
    ssid = result.ssid
    print(f"SSID: {ssid}, BSSID: {bssid}")

'''