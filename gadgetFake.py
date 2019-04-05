from gadgetpy import Gadget,MassStorage,Network,Config

class FakeGadget(Gadget):
    def __init__(self,name,path=None,write=True):
        self.doesExists = False
        Gadget.__init__(self,name,'/tmp/',False)
        self.doesExists = True
        self.mounted=False
        pass
    def isMounted(self):
        return self.mounted
    def exists(self):
        return self.doesExists
    def write(self):
        pass
    def buildPath(self):
        pass
    def activate(self,pointer):
        self.mounted=True
    def deactivate(self):
        self.mounted=False

class FakeMassStorage(MassStorage):
    def __init__(self,name):
        MassStorage.__init__(self,name)
    def write(self,path):
        pass
    def buildPath(self,path):
        pass

class FakeNetwork(Network):
    def __init__(self,name):
        Network.__init__(self,name)
        pass
    def write(self,path):
        pass
    def buildPath(self,path):
        pass

class FakeConfig(Config):
    def __init__(self,name):
        Config.__init__(self,name)
        pass
    def write(self,path):
        pass
    def buildPath(self,path):
        pass
