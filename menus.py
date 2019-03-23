import time
import os,signal

import subprocess

import signal

from libs.menu import Menu, PyGameMenuController, MenuLine, MenuEntry, MenuText, MenuCustom, ProgressMenu
from libs.progress import ProgressImage

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def ip_render():
    cmd = "hostname -I | cut -d\' \' -f1"
    return subprocess.check_output(cmd, shell = True)

def cpu_render():
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    return subprocess.check_output(cmd, shell = True)

def cmd_render():
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    return subprocess.check_output(cmd, shell = True)

def disk_render():
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    return subprocess.check_output(cmd, shell = True)

def disable_usb_network():
    cmd = "sudo ifconfig usb0 down"
    os.system(cmd)

def enable_usb_network():
    cmd = "sudo ifconfig usb0 up"
    os.system(cmd)

def disable_wifi_network():
    cmd = "sudo ifconfig wifi0 down"
    os.system(cmd)

def enable_wifi_network():
    cmd = "sudo ifconfig wifi0 up"
    os.system(cmd)

def enable_gadget():
    cmd = "echo '20980000.usb' | tee /sys/kernel/config/usb_gadget/provkey/UDC"
    os.system(cmd)

def disable_gadget():
    cmd = "echo '' | tee /sys/kernel/config/usb_gadget/provkey/UDC"
    os.system(cmd)

def getMenus(shutdown):
    root = Menu()
    load = ProgressMenu('images/scale.bmp',50,root)
    setup = Menu()
    network = Menu()
    wifi = Menu()
    usbNet = Menu()
    usb = Menu()
    info = Menu(True,4)
    root.addLine(MenuEntry('Setup',setup))
    root.addLine(MenuLine('Exit',shutdown))
    setup.addLine(MenuEntry('Status',info))
    setup.addLine(MenuEntry('Network',network))
    setup.addLine(MenuEntry('Gadget',usb))
    setup.addLine(MenuEntry('back',root))
    network.addLine(MenuEntry('Wifi',wifi))
    network.addLine(MenuEntry('Usb',usbNet))
    network.addLine(MenuEntry('back',setup))
    wifi.addLine(MenuLine('Wifi Off',disable_wifi_network))
    wifi.addLine(MenuLine('Wifi On',enable_wifi_network))
    wifi.addLine(MenuEntry('back',network))
    usbNet.addLine(MenuLine('Usb Off',disable_usb_network))
    usbNet.addLine(MenuLine('Usb On',enable_usb_network))
    usbNet.addLine(MenuEntry('back',network))
    usb.addLine(MenuLine('Enable Gadget',enable_gadget))
    usb.addLine(MenuLine('Disable Gadget',disable_gadget))
    usb.addLine(MenuEntry('back',setup))
    info.addLine(MenuCustom(ip_render),False)
    info.addLine(MenuCustom(cpu_render),False)
    info.addLine(MenuCustom(cmd_render),False)
    info.addLine(MenuCustom(disk_render),False)
    info.addLine(MenuEntry('back',setup))
    return load
