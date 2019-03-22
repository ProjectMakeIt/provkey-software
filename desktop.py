import time
import signal

from menus import getMenus
from libs.menu import PyGameMenuController

def killhandle(signum, frame):
  exit(0)

def shutdown():
    killhandle(0,0);

load = getMenus(shutdown)
controller = PyGameMenuController(load)
load.setCtl(controller)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, killhandle)
    try:
      while True:
        controller.loop()
        time.sleep(0.05)
    except (KeyboardInterrupt, SystemExit):
      killhandle(1,0)
