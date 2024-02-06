import network
import time
import ujson

# Function to load WiFi configuration from JSON file
def load_wifi_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = ujson.load(file)
        return config
    except Exception as e:
        print("Error loading WiFi configuration:", e)
        return None


def do_connect(wifi_config: str):
    # Load WiFi configuration from JSON file
    config = load_wifi_config(wifi_config)

    ssid = config["ssid"]
    password = config['password']
    wlan = network.WLAN(network.STA_IF)
    #restarting wifi to avoid any errors
    wlan.active(False)
    time.sleep(0.5)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
