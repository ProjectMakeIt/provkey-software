import os

# USB Gadget Class
# ----
# Manages a single usb gadget for usage on things like RPi Zero
# Parameters:
# name: Name of the gadget.  this is what goes into the usb_gadget folder.
# path: Path to the usb_gadget folder.  Under /sys/kernel/config/ by default in Raspbian, but can be changed
#       by mounting cfgfs somewhere else.
# write: Defaults to True. Whether or not to immediatly create the gadget folder when initializing the gadget.

class Gadget:
    def __init__(self,name,path,write=True):
        self.idVendor = "0x1d6b"
        self.idProduct = "0x0104"
        self.bcdDevice = "0x0100"
        self.bcdUSB = "0x0200"
        self.serialnumber="fedcba9876543210"
        self.manufacture="Lorium Ipsum"
        self.product="Python Gadget"
        self.name = name
        self.path = os.path.join(path,name)
        self.configs = {}
        self.functions = {}
        stringsPath = os.path.join('strings','0x409')
        self.files = {
                'idVendor': 'idVendor',
                'idProduct': 'idProduct',
                'bcdDevice': 'bcdDevice',
                os.path.join(stringsPath,'manufacturer'):'manufacturer',
                os.path.join(stringsPath,'serialnumber'):'serialnumber',
                os.path.join(stringsPath,'product'):'product',
        }
        if self.exists():
            raise GadgetExists()
        if write:
            self.buildPaths()
            self.write()
    # Write out gadget data
    # Should be called when you set or update any of the gadget, function, or config info
    # Will throw an error if the gadget is currenty enabled
    def write():
        if self.isMounted():
            raise GadgetMounted()
            return
        for fName,name in self.files.items():
            with open(os.path.join(self.path,fName),'w') as f:
                f.write(self[name])
        for function in self.functions:
            function.write(self.path)
        for config in self.configs:
            config.write(self.path)
    # Build inital paths
    # Should only be called once to generate the inital paths.
    def buildPaths(self):
        if self.exists():
            raise GadgetExists()
        # NOTE: 0x409 is for English.  Should eventually add support for other languages at
        # some point
        stringsPath = os.path.join(self.path,'strings','0x409')
        os.mkdir(stringsPath)
    # Will attempt to bind the gadget to a usb pointer.  Will first check to see if the pointer
    # exists, then verify that it is currently not in use.
    def activate(self,pointer):
        if not verifyPointer(pointer):
            raise PointerMounted()
        os.system('echo "%s" > %s' % pointer, os.path.join(self.path,'UDC'))
    def deactivate(self):
        os.system('echo "" > %s' % os.path.join(self.path,'UDC'))
    # Add a config to the gadget
    def addConfig(self,config):
        self.configs[config.name] = config
        config.buildPath(self.path)
    # Add a function to the gadget
    def addFunction(self,function):
        self.functions[function.name] = function
        function.buildPath(self.path)

# Gadget Config
# ----
# Gadgets can have multiple configs when in use
# This class handles creating said configs, and maintaining which functions
# are in use by the config
# Parameters:
# name: The name to use for the config.  this must be in the form of 'c.#' to
#       work correctly
class Config:
    def __init__(self,name):
        if not verifyName(self.name):
            raise GadgetInvalid("Attempted to create a config with an invalid name")
        self.name = name
        self.functions = []
    def write(self,path):
        myPath = os.path.join(path,'configs',name)
        existingFunctions = [f for f in os.listdir(myPath if verifyName(f)]
        for func in existingFunctions:
            if not func in self.functions:
                os.remove(os.path.join(myPath,func))
        for func in self.functions:
            if not os.path.exists(os.path.join(myPath,func)):
                os.symlink(os.path.join(path,'functions',func),myPath)
        pass
    # NOTE: This does not currently verify if the function is part of the correct
    #       gadget.  Wierd things may happen if you try to cross gadgets
    def addFunction(self,function):
        self.functions.append(function.name)
        pass

# Gadget Function 
# ----
# Gadgets can have multiple functions per config
# This class defines the basic function type.
# Please note that this class doesn't implement any
# function features or type, and so can't be directly implemented
# Parameters: 
# name: Name of the function device.  This doesn't include the type,
#       and must be formated as "<name>#". E.g. "usb0"
class Function:
    def __init__(self,name):
        if not self.type:
            raise GadgetInvalid("Attempted to create a raw function element")
        self.name = self.type+"."+name
        if not verifyName(self.name):
            raise GadgetInvalid("Attempted to create a function with an invalid name")
    def write(self,path):
        pass
    def buildPath(self,path):
        functionPath = os.path.join(path,self.name)
        os.mkdir(functionPath)

# Mass Storage Function
# ----
# Implementation of the Mass Storage Function
# Can handle passing a single file as a mass storage partition
# Currently doesn't implement any support for additional luns, but will auto
# create the first one.
# Parameters:
# No additional parameters from Function
class MassStorage(Function):
    def __init__(self,name):
        self.type="mass_storage"
        Function.__init__(self,name)
        self.cdrom = False
        self.readOnly = False
        self.image = ""
        self.nofua = False
        self.removable = False
    def write(self,path):
        lunPath = os.path.join(path,'lun.0')
        # NOTE: Cant write to the file using open, so we are using os.system.  Need to see what is needed
        # to fix this.
        os.system('echo "%s" > %s' % self.image, os.path.join(lunPath,'file'))
        if self.cdrom:
            os.system('echo "1" > %s' % self.image, os.path.join(lunPath,'cdrom'))
        else:
            os.system('echo "0" > %s' % self.image, os.path.join(lunPath,'cdrom'))
        if self.readOnly:
            os.system('echo "1" > %s' % self.image, os.path.join(lunPath,'ro'))
        else:
            os.system('echo "0" > %s' % self.image, os.path.join(lunPath,'ro'))
        if self.nofua:
            os.system('echo "1" > %s' % self.image, os.path.join(lunPath,'nofua'))
        else:
            os.system('echo "0" > %s' % self.image, os.path.join(lunPath,'nofua'))
        if self.removable:
            os.system('echo "1" > %s' % self.image, os.path.join(lunPath,'removable'))
        else:
            os.system('echo "0" > %s' % self.image, os.path.join(lunPath,'removable'))

# Basic Gadget Exception
class GadgetException(Exception):
    pass

# Attempting to create an existing gadget.  Need to remove the old one first.
class GadgetExists(GadgetException):
    pass

# Attempting to update a gadget when it is already mounted.  Unmount it first.
class GadgetMounted(GadgetException):
    pass

# Attempting to mount a gadget to a pointer that either already is mounted,
# or doesn't exist
class PointerMounted(GadgetException):
    pass

def verifyName(name):
    parts = name.split('.')
    return len(parts)==2
