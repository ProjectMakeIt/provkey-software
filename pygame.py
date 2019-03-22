import time
import signal

from menus import load

def killhandle(signum, frame):
  exit(0)

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
