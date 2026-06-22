import paho.mqtt.client as mqtt
import time
import json

# --- LLM Simulation ---
# This function simulates Claude's role: taking natural language and converting it to structured commands.
# In a real scenario, Claude would perform complex natural language understanding and intent extraction.
def simulate_llm_parse(natural_language_input):
    """
    Simulates an LLM parsing natural language into MQTT topics and payloads.
    """
    input_lower = natural_language_input.lower()

    if "oturma odası ışıklarını aç" in input_lower or "turn on living room lights" in input_lower:
        return "home/living_room/light/set", "ON"
    elif "oturma odası ışıklarını kapat" in input_lower or "turn off living room lights" in input_lower:
        return "home/living_room/light/set", "OFF"
    elif "oturma odası ışıklarını kıs" in input_lower or "dim living room lights" in input_lower:
        # Assuming a default dim level for simplicity; a real LLM could extract specific percentages.
        return "home/living_room/light/brightness/set", "50" # 50%
    elif "sakinleştirici müzik çal" in input_lower or "play calming music" in input_lower:
        return "home/media_player/living_room/play", "calming_playlist"
    elif "yatak odası ışıklarını %30 yap" in input_lower or "set bedroom lights to 30%" in input_lower:
        return "home/bedroom/light/brightness/set", "30"
    else:
        return None, None # LLM couldn't understand or no action defined

# --- MQTT Client Setup (Simulating Home Assistant / IoT Device Listener) ---
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    # Subscribing to all commands under 'home/' topic.
    # This simulates Home Assistant or devices listening for commands published by the LLM.
    client.subscribe("home/#") # Wildcard subscription for all home automation commands

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"\n[{time.strftime('%H:%M:%S')}] Home Assistant/Device received command:")
    print(f"  Topic: {msg.topic}")
    print(f"  Payload: {msg.payload.decode()}")

    # Simulate Home Assistant processing the command based on topic and payload.
    topic_parts = msg.topic.split('/')
    if len(topic_parts) >= 3 and topic_parts[0] == 'home':
        device_context = topic_parts[1] # e.g., living_room, bedroom
        component_type = topic_parts[2] # e.g., light, media_player
        action_type = topic_parts[3] if len(topic_parts) > 3 else "unknown"

        payload = msg.payload.decode()

        if component_type == "light" and action_type == "set":
            print(f"    -> Action: Setting {device_context} {component_type} to {payload}")
        elif component_type == "light" and action_type == "brightness":
            print(f"    -> Action: Setting {device_context} {component_type} brightness to {payload}%")
        elif component_type == "media_player" and action_type == "play":
            print(f"    -> Action: Playing '{payload}' on {device_context} {component_type}")
        else:
            print(f"    -> Action: Unhandled command for {device_context}/{component_type}: {action_type} with payload {payload}")
    print("-" * 30)

# Create an MQTT client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to a public MQTT broker (requires internet connection).
# In a real Home Assistant setup, this would typically be your local Mosquitto broker.
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT client loop in a non-blocking way.
# This allows the script to publish messages while also listening for incoming messages.
client.loop_start()

print("Simulating smart home commands via Claude (LLM) and MQTT...")
print("Type 'exit' to quit.")
print("-" * 30)

# --- Main loop for simulating user interaction and LLM output ---
while True:
    user_input = input("You (to Claude): ")
    if user_input.lower() == 'exit':
        break

    # Simulate Claude processing the natural language input
    topic, payload = simulate_llm_parse(user_input)

    if topic and payload:
        print(f"\n[LLM Simulation] Claude understood: '{user_input}'")
        print(f"[LLM Simulation] Translating to MQTT: Topic='{topic}', Payload='{payload}'")
        # Publish the structured command via MQTT
        client.publish(topic, payload)
        time.sleep(0.5) # Give a brief moment for the message to be processed by the subscriber
    else:
        print("[LLM Simulation] Claude couldn't understand or no action defined for that phrase.")
    print("-" * 30)

# Clean up
client.loop_stop()
client.disconnect()
print("Exiting.")
