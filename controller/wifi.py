import network
import time
from config.env_reader import ConfigReader as conf_reader


def connect():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    if sta.isconnected():
        print("WiFi: already connected —", sta.ifconfig()[0])
        return sta

    print("WiFi: connecting to", conf_reader.get("WIFI_SSID"))
    sta.connect(conf_reader.get("WIFI_SSID"), conf_reader.get("WIFI_PASSWORD"))

    deadline = time.time() + 20
    while not sta.isconnected():
        if time.time() > deadline:
            raise RuntimeError("WiFi: connection timed out")
        time.sleep(0.5)

    ip = sta.ifconfig()[0]
    print("WiFi: connected —", ip)
    return sta
