# Beer Temperature Monitor

A Python service that relays a Raspberry Pi temperature to an external service for processing.

More info to come later!

# Requirements
- Raspberry Pi (current development on Raspberry Pi Zero)
- Adafruit MCP9808 Temperature sensor

# Install
1. Download repo
2. Go into project folder
  - cd beer_temp_monitor
3. Install required packages
  - pip install -r requirements.txt
4. Run the monitor! (Currently, receiving server must be up and running!)
  - python src/beer_temp_monitor.py
