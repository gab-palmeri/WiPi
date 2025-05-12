import subprocess
import os

AP_NAME = os.getenv("AP_NAME", "RaspberryPi")
AP_PASS = os.getenv("AP_PASS", "raspberry")

def scan_wifi():
    #execute command nmcli device wifi rescan
    try:
        output = subprocess.run(["sudo", "nmcli", "device", "wifi", "rescan"])
        output = subprocess.run(["nmcli", "-t", "-f", "SSID", "dev", "wifi"], stdout=subprocess.PIPE).stdout
        return list(set([line.strip() for line in output.decode().splitlines() if line.strip()]))
    except subprocess.CalledProcessError as e:
        print(f"Error during WiFi scan: {e.stderr.decode()}")
        return None

def get_saved_networks():
    #get saved networks with nmcli in wifi, and the actual connected one
    try:
        #get the actual connected one
        output = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'device', 'wifi'], stdout=subprocess.PIPE).stdout
        connected_network = [line.strip().split(":")[1] for line in output.decode().splitlines() if line.strip() and "yes" in line][0]

        output = subprocess.run(["nmcli", "-t", "-f", "NAME,type", "connection", "show"], stdout=subprocess.PIPE).stdout
        saved_networks = list(set([line.strip().split(":")[0] for line in output.decode().splitlines() if line.strip() and "wireless" in line]))
        
        if "Hotspot" in saved_networks:
            saved_networks.remove("Hotspot")
        if connected_network in saved_networks:
            saved_networks.remove(connected_network)
        
        return connected_network, saved_networks

    except subprocess.CalledProcessError as e:
        print(f"Error during saved networks fetch: {e.stderr.decode()}")
        return None, None

def connect_to_wifi(ssid, password):
    try:
        subprocess.run(["sudo", "nmcli", "connection", "delete", "Hotspot"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "nmcli", "dev", "wifi", "connect", ssid, "password", password], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def forget_wifi(ssid):
    try:
        subprocess.run(["sudo", "nmcli", "connection", "delete", ssid], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def switch_to_wifi(ssid):
    try:
        subprocess.run(["sudo", "nmcli", "connection", "delete", "Hotspot"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "nmcli", "connection", "up", ssid], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_access_point():
    try:
        subprocess.run(["sudo", "nmcli", "dev", "wifi", "hotspot", "ifname", "wlan0", "ssid", AP_NAME, "password", AP_PASS], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
