#!/bin/bash

# Funzione per controllare la connessione internet
check_internet() {
  if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
    echo "Connected"
    return 0
  else
    echo "No internet connection"
    return 1
  fi
}

# Funzione per avviare l'hotspot
start_hotspot() {
  echo "Starting Hotspot..."
  sudo nmcli dev wifi hotspot ifname wlan0 ssid RaspberryPi password raspberry
}

# Verifica stato di NetworkManager e connessione
if systemctl is-active --quiet NetworkManager; then
  if nmcli -t -f ACTIVE,SSID dev wifi | grep -q '^yes'; then
    echo "Wi-Fi connected"
    if check_internet; then
      echo "Internet connection is active"
    else
      echo "Internet connection is not available"
      start_hotspot
    fi
  else
    echo "Wi-Fi is not connected"
    start_hotspot
  fi
else
  echo "NetworkManager is not active"
  start_hotspot
fi

# Avvio del webserver alla fine
echo "Starting Flask webserver..."
cd /home/gab/dashboard
source venv/bin/activate
python3 app.py
