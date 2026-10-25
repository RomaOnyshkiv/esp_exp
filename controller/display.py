from machine import Pin, I2C
from lbs import ssd1306



class Disp:
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)



    def show_time(self, info_to_show):
        self.oled.fill(0)
        self.oled.text("## INFO ##", 0, 0)
        self.oled.text("", 0, 16)
        self.oled.text(info_to_show, 0, 32)

        self.oled.show()