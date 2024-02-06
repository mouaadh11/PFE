from umqtt.simple import MQTTClient
import ujson
# Function to load Broker configuration from JSON file
def load_broker_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = ujson.load(file)
        return config
    except Exception as e:
        print("Error loading broker configuration:", e)
        return None

# Load Broker configuration from JSON file
config = load_broker_config("broker_config.json")

CLIENT_ID = config["client_id"]
BROKER_ADDRESS = config["broker_adr"]
TOPIC = config["topic"]

def setUp() :    
    mqttc = MQTTClient(CLIENT_ID, BROKER_ADDRESS)
    return mqttc

def connect( mqttc ) :
    mqttc.connect()

def send_data(mqttc ,ir_reading, red_reading, beats, current_time) :
      mqttc.publish(TOPIC, f"{ir_reading},{red_reading},{beats},{current_time})".encode())

