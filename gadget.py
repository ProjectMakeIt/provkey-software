import os

GADGET_URL = "/sys/kernel/config/usb_gadget"
device_base = os.path.join(GADGET_URL, 'provkey')

def disable():
    os.system('echo "" > %s' % os.path.join(device_base, 'UDC'))    
def enable():
    os.system('ls /sys/class/udc > %s' % os.path.join(device_base, 'UDC'))    