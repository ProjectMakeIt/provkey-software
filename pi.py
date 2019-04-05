import time,os
import signal
import gadget

from RPi import GPIO

import Adafruit_SSD1306

from libs.menu import OledMenuController
from menus import getMenus

def killhandle(signum, frame):
  GPIO.cleanup()
  exit(0)

def shutdown():
    os.system('sudo shutdown -h now')
    killhandle(0,0);


gadget.initPi()
load = getMenus(shutdown)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
controller = OledMenuController(load,disp,17,22,5,6)
load.setCtl(controller)

if __name__ == "__main__":
    disp.begin()
    disp.clear()
    disp.display()
    signal.signal(signal.SIGTERM, killhandle)
    try:
      while True:
        controller.loop()
    except (KeyboardInterrupt, SystemExit):
      killhandle(1,0)
