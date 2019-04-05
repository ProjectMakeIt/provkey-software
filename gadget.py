import os
import gadgetpy
import gadgetFake

def initPi():
    global gadget
    global fs
    global network
    gadget = gadgetpy.Gadget('provkey')
    fs = gadgetpy.MassStorage('usb0')
    network = gadgetpy.Network('usb0')
    config = gadgetpy.Config('c.1')
    gadget.addFunction(fs)
    gadget.addFunction(network)
    gadget.addConfig(config)
    config.addFunction(fs)
    gadget.addFunction(network)
    gadget.write()

def initDesktop():
    global gadget
    global fs
    global network
    gadget = gadgetFake.FakeGadget('provkey')
    fs = gadgetFake.FakeMassStorage('usb0')
    network = gadgetFake.FakeNetwork('usb0')

pointer = ""

def setUSB(point):
    pointer = point

def disable():
    gadget.deactivate()

def enable():
    gadget.activate(pointer)

def changeImage(filename):
    gadget.deactivate()
    fs.image = filename
    gadget.activate(pointer)
