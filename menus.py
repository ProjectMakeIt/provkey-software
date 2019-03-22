import time
import os,signal

import subprocess

import signal

from menu import Menu, PyGameMenuController, MenuLine, MenuEntry, MenuText, MenuCustom, ProgressMenu
from progress import ProgressImage

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

root = Menu()
load = ProgressMenu('scale.bmp',50,root)
setup = Menu()
info = Menu(True,4)
root.addLine(MenuEntry('Setup',setup))
setup.addLine(MenuEntry('Status',info))
setup.addLine(MenuEntry('back',root))
info.addLine(MenuCustom(ip_render),False)
info.addLine(MenuCustom(cpu_render),False)
info.addLine(MenuCustom(cmd_render),False)
info.addLine(MenuCustom(disk_render),False)
info.addLine(MenuEntry('back',setup))
