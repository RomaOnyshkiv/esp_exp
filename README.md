# ESP32 display server

This MicroPython project runs on an ESP32 and displays messages on a 128x64
SSD1306 OLED. The ESP32 serves `/health` and accepts display updates at
`POST /msg` with a JSON body such as `{"info":"Hello"}`.

## Run in Wokwi

1. Install the **Wokwi for VS Code** extension.
2. Open this project in VS Code and choose **Wokwi: Start Simulator** from the
   Command Palette. Keep the simulator tab visible while interacting with it.
3. Ensure the MicroPython firmware configured in `wokwi.toml` exists at the
   configured path.
4. Run `make install` once to install `mpremote` in the project virtualenv.
5. Run `make wokwi` to upload the project and start `main.py` on the simulated
   ESP32. The Wokwi-specific `.env.example` is uploaded as `/.env`; it connects
   to the `Wokwi-GUEST` network and listens on port `80`.

The diagram connects the SSD1306 I2C pins to GPIO 22 (SCL) and GPIO 21 (SDA),
matching `controller/display.py`. The simulated board's serial output shows
the assigned IP address and server startup status.

### Send requests from your terminal

Wokwi's default Public Gateway does not allow incoming connections. To reach
the simulated server, install and run the [Wokwi IoT Gateway](https://github.com/wokwi/wokwigw/releases/latest)
(available to Wokwi Club members), then enable **Private Wokwi IoT Gateway**
in the Wokwi editor using its Command Palette. The gateway forwards
`http://localhost:9080` to port `80` on the simulated ESP32. This project
therefore uses port `80` in its Wokwi `.env.example`.

With the simulator and Private Gateway running, use these commands in another
terminal:

```sh
make wokwi-health
make wokwi-message
make wokwi-message WOKWI_MESSAGE="Build complete"
```

Equivalent `curl` commands:

```sh
curl http://localhost:9080/health
curl -X POST http://localhost:9080/msg \
  -H 'Content-Type: application/json' \
  -d '{"info":"Hello from terminal"}'
```

The message appears on the simulated OLED. Wokwi's Private Gateway currently
requires Chrome, Firefox, or Edge; Safari is not supported.

To upload files without starting the server, run `make wokwi-upload`. If your
firmware is stored elsewhere, update the `firmware` path in `wokwi.toml`.

## Run on a physical ESP32

Copy `.env.example` to `.env`, set `WIFI_SSID`, `WIFI_PASSWORD`, and
`SERVER_PORT`, then use the existing `make flash` workflow.
