.PHONY: install flash reset getpid offscreen restart wokwi-upload wokwi wokwi-health wokwi-message

VENV     := .venv
PYTHON   := $(VENV)/bin/python
PIP      := $(VENV)/bin/pip
WOKWI_PORT ?= port:rfc2217://localhost:4000
WOKWI_HTTP_URL ?= http://localhost:9080
WOKWI_MESSAGE ?= Hello from terminal
ESP_PORT ?= /dev/tty.usbserial-0001
CHIP	 := esp32
BAUD	 := 115200
FRMWR	 := ESP32_GENERIC-20260824-v1.29.0.bin
PID		 ?= none
AMPY 	 := ampy --port $(ESP_PORT)


# ── Host  ──────────────────────────────────────

install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate


# ── ESP32 ─────────────────────────────────

flash:
	$(AMPY) mkdir config --exists-okay
	$(AMPY) mkdir controller --exists-okay
	$(AMPY) mkdir lbs --exists-okay
	$(AMPY) mkdir server --exists-okay
	$(AMPY) put config/env_reader.py config/env_reader.py
	$(AMPY) put config/env_parser.py config/env_parser.py
	$(AMPY) put .env .env
	$(AMPY) put controller/display.py controller/display.py
	$(AMPY) put controller/wifi.py controller/wifi.py
	$(AMPY) put lbs/ssd1306.py lbs/ssd1306.py
	$(AMPY) put server/DispServer.py server/DispServer.py
	$(AMPY) put main.py main.py
	@echo "ESP32 flashed. Reset the board to start."

clear:
	esptool --port $(ESP_PORT) --baud $(BAUD) erase-flash
	esptool --chip $(CHIP) --port $(ESP_PORT) --baud $(BAUD) write-flash -z 0x1000 ../firmware/$(FRMWR)

reset:
	esptool --port $(ESP_PORT) run

screen:
	screen $(ESP_PORT) $(BAUD)

getpid:
	screen -ls | grep ".tt"

offscreen:
	screen -S $(PID) -X quit

restart: clear flash reset

wokwi-upload: install
	$(PYTHON) -m mpremote connect $(WOKWI_PORT) fs cp -r config : + fs cp -r controller : + fs cp -r lbs : + fs cp -r server : + fs cp main.py :main.py + fs cp .env.example :.env

wokwi: wokwi-upload
	$(PYTHON) -m mpremote connect $(WOKWI_PORT) run main.py

wokwi-health:
	curl --fail --show-error "$(WOKWI_HTTP_URL)/health"

wokwi-message:
	curl --fail --show-error -X POST "$(WOKWI_HTTP_URL)/msg" \
		-H "Content-Type: application/json" \
		--data '{"info":"$(WOKWI_MESSAGE)"}'
