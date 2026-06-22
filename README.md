# Claude MQTT Home Assistant Simulation

This example Python script demonstrates the core concept of integrating an LLM (simulated as "Claude") with MQTT for smart home automation, as described in the article. It simulates an LLM parsing natural language commands into structured MQTT messages, which are then published and received by a simulated Home Assistant or IoT device listener. This showcases how conversational input can drive device actions via a message queueing protocol.

## Language

`python`

## How to Run

1. Install the `paho-mqtt` library: `pip install paho-mqtt`
2. Run the script: `python main.py`
3. Type commands like "Turn on living room lights" (or "oturma odası ışıklarını aç") and observe the simulated Home Assistant/device actions. (Requires an internet connection to reach the public MQTT broker).

## Original Article

This example accompanies the Turkish article: [Claude, MCP ve Home Assistant ile Akıllı Ev Otomasyonu](https://fatihsoysal.com/blog/claude-mcp-ve-home-assistant-ile-akilli-ev-otomasyonu/).

## License

MIT — see [LICENSE](LICENSE).
