import time
import os,signal

import subprocess

import signal

from libs.menu import Menu, PyGameMenuController, MenuLine, MenuEntry, MenuText, MenuCustom, ProgressLine, LoaderMenu, TitleMenu
from libs.progress import ProgressImage
from libs.config import Config, ConfigJson

import gadget

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

def enable_gadget():
    gadget.enable()

def disable_gadget():
    gadget.disable()

def generate_setup(name,setup):
    menu = Menu()
    line = MenuEntry(name,menu)
    menu.addLine(MenuLine('Switch Image',lambda: gadget.changeImage(setup.image)))
    return line

def get_setups(config):
    menu = Menu()
    for name,setup in config.getAll().items():
       menu.addLine(generate_setup(name,setup))
    return menu

def setupConfig():
    config = Config()
    config.setStorage(ConfigJson('config.json'))
    if os.path.exists('config.json'):
        config.load()
    return config

def titleLine():
    return "Test Title Screen"
    
def getMenus(shutdown):
    config = setupConfig()
    root = Menu()
    load = LoaderMenu('images/scale.bmp',50,root)
    setup = Menu()
    usb = Menu()
    info = Menu(True,4)
    testMenu = TitleMenu('Test Menu')
    testTitleMenu = TitleMenu(MenuCustom(titleLine))
    progress = Menu()
    progressLine = ProgressLine(10)
    progressLine.update(9)
    progress.addLine(progressLine)
    progress.addLine(MenuEntry('back',testMenu))
    root.addLine(MenuEntry('Setup',setup))
    root.addLine(MenuEntry('Test Menu',testMenu))
    root.addLine(MenuEntry('Images',get_setups(config)))
    root.addLine(MenuLine('Exit',shutdown))
    testMenu.addLine(MenuEntry('Test Loader',load))
    testMenu.addLine(MenuEntry('Test Progress',progress))
    testMenu.addLine(MenuEntry('Test Title',testTitleMenu))
    testMenu.addLine('Test4')
    testMenu.addLine('Test5')
    testMenu.addLine('Test6')
    testMenu.addLine('Test7')
    testMenu.addLine('Test8')
    testMenu.addLine('Test9')
    testMenu.addLine('Test10')
    testMenu.addLine('Test11')
    testMenu.addLine('Test12')
    testMenu.addLine(MenuEntry('back',root))
    testTitleMenu.addLine('Test1')
    testTitleMenu.addLine(MenuEntry('back',testMenu))
    setup.addLine(MenuEntry('Status',info))
    setup.addLine(MenuEntry('Gadget',usb))
    setup.addLine(MenuEntry('back',root))
    usb.addLine(MenuLine('Enable Gadget',enable_gadget))
    usb.addLine(MenuLine('Disable Gadget',disable_gadget))
    usb.addLine(MenuEntry('back',setup))
    info.addLine(MenuCustom(ip_render),True)
    info.addLine(MenuCustom(cpu_render),True)
    info.addLine(MenuCustom(cmd_render),True)
    info.addLine(MenuCustom(disk_render),True)
    info.addLine(MenuEntry('back',setup))
    return load
