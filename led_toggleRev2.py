#!/usr/bin/env python3
"""
LED Toggle Server for Raspberry Pi 4
-------------------------------------
Toggles an LED on GPIO 17 via a single HTTP endpoint.

Wiring:
  GPIO 17 (Pin 11) --> LED Anode (+)
  LED Cathode (-)  --> 330Ω resistor --> GND (Pin 6)

Usage:
  pip3 install flask RPi.GPIO
  python3 led_toggle.py

Then visit: http://<your-pi-ip>:5000
Or use curl: curl http://localhost:5000
"""

import RPi.GPIO as GPIO
from flask import Flask, jsonify

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
LED_PIN = 17        # BCM pin number (change if needed)
HOST    = "0.0.0.0" # Listen on all interfaces so any device on the network can reach it
PORT    = 5000

# ---------------------------------------------------------------------------
# GPIO Setup
# ---------------------------------------------------------------------------
GPIO.setmode(GPIO.BCM)          # Use BCM pin numbering
GPIO.setup(LED_PIN, GPIO.OUT)   # Set LED pin as output
GPIO.output(LED_PIN, GPIO.LOW)  # Start with LED off

led_state = False  # Track current state in memory

# ---------------------------------------------------------------------------
# Flask App
# ---------------------------------------------------------------------------
app = Flask(__name__)


@app.route("/toggle", methods=["GET", "POST"])
def toggle_led():
    """Toggle the LED on/off and return the new state as JSON."""
    global led_state

    led_state = not led_state                          # Flip the state
    GPIO.output(LED_PIN, GPIO.HIGH if led_state else GPIO.LOW)

    return jsonify({
        "status": "ok",
        "led":    "ON" if led_state else "OFF",
        "pin":    LED_PIN,
    })


@app.route("/state", methods=["GET"])
def get_state():
    """Return the current LED state without changing it."""
    return jsonify({
        "status": "ok",
        "led":    "ON" if led_state else "OFF",
        "pin":    LED_PIN,
    })


@app.route("/", methods=["GET"])
def index():
    """Simple HTML control page — status updates automatically via JS polling."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Light Control</title>
  <style>
    body {{
      font-family: monospace;
      background: #0f172a;
      color: #e2e8f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      gap: 2rem;
    }}
    h1 {{ font-size: 1.5rem; letter-spacing: 0.1em; color: #94a3b8; margin: 0; }}
    .bulb {{
      width: 120px;
      height: 120px;
      border-radius: 50%;
      background: #6b7280;
      box-shadow: 0 0 0 0 #000;
      transition: background 0.3s ease, box-shadow 0.3s ease;
    }}
    .bulb.on {{
      background: #22c55e;
      box-shadow: 0 0 60px 20px #22c55e;
    }}
    .label {{
      font-size: 2rem;
      font-weight: bold;
      color: #6b7280;
      transition: color 0.3s ease;
    }}
    .label.on {{ color: #22c55e; }}
    button {{
      padding: 0.75rem 2rem;
      background: #1e293b;
      color: #38bdf8;
      border: 1px solid #38bdf8;
      border-radius: 6px;
      font-size: 1rem;
      font-family: monospace;
      letter-spacing: 0.05em;
      cursor: pointer;
      transition: background 0.2s;
    }}
    button:hover {{ background: #0ea5e9; color: #fff; }}
    .info {{ color: #475569; font-size: 0.85rem; }}
  </style>
</head>
<body>
  <h1>🔌 GPIO LIGHT CONTROL. Press Button to Change Light.</h1>
  <div class="bulb" id="bulb"></div>
  <div class="label" id="label">Checking...</div>
  <button id="toggleBtn" onclick="toggleLight()">Change Light</button>
  <div class="info">GPIO Pin: BCM {LED_PIN} &nbsp;|&nbsp; GET /toggle &nbsp;|&nbsp; GET /state</div>

  <script>
    // Fetch the current LED state and update the UI
    function updateStatus() {{
      fetch('/state')
        .then(response => response.json())
        .then(data => {{
          const isOn = data.led === 'ON';
          const bulb  = document.getElementById('bulb');
          const label = document.getElementById('label');

          bulb.classList.toggle('on', isOn);
          label.classList.toggle('on', isOn);
          label.textContent = 'Light is ' + data.led;
        }})
        .catch(() => {{
          document.getElementById('label').textContent = 'Connection error';
        }});
    }}

    // Call /toggle via fetch so the page never navigates away
    function toggleLight() {{
      fetch('/toggle')
        .then(response => response.json())
        .then(data => {{
          const isOn = data.led === 'ON';
          const bulb  = document.getElementById('bulb');
          const label = document.getElementById('label');

          bulb.classList.toggle('on', isOn);
          label.classList.toggle('on', isOn);
          label.textContent = 'Light is ' + data.led;
        }})
        .catch(() => {{
          document.getElementById('label').textContent = 'Toggle failed';
        }});
    }}

    // Update immediately on page load, then every 1 second
    updateStatus();
    setInterval(updateStatus, 1000);
  </script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Cleanup on exit
# ---------------------------------------------------------------------------
import atexit

@atexit.register
def cleanup():
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO cleaned up.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"LED Toggle Server running on http://{HOST}:{PORT}")
    print(f"  Toggle : http://<pi-ip>:{PORT}/toggle")
    print(f"  State  : http://<pi-ip>:{PORT}/state")
    print(f"  UI     : http://<pi-ip>:{PORT}/")
    app.run(host=HOST, port=PORT, debug=False)
