from utils import wifi

# Handlers Methods
def handle_get_wifi():
    connected_network, saved_networks = wifi.get_saved_networks()
    available = wifi.scan_wifi()

    saved_and_available = [ssid for ssid in saved_networks if ssid in available]
    saved_not_available = [ssid for ssid in saved_networks if ssid not in available]

    filtered_available = [w for w in available if w != connected_network and w not in saved_networks]

    return connected_network, saved_and_available, saved_not_available, filtered_available

def handle_post_wifi(ssid, password):
    message = ""
    
    if wifi.connect_to_wifi(ssid, password):
        message = f"Connected to {ssid}!"
    else:
        message = "Connection error."

    return message

def handle_delete_wifi(ssid):
    if wifi.forget_wifi(ssid):
        message = f"{ssid} forgotten!"
    else:
        message = "Operation error."
    
    return message

def handle_switch_wifi(ssid):
    if wifi.switch_to_wifi(ssid):
        message = f"Switched to {ssid} network!"
    else:
        message = "Error during connection switch."

def handle_ap_mode():
    if wifi.create_access_point():
        message = f"Access point created"
    else:
        message = "Errore during access point creation."