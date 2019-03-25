import os,json
from attrdict import AttrDict

class Config:
    def __init__(self):
        self._config_object = {}
        self._storage = None
    def setStorage(self,storage):
        self._storage = storage
    def load(self):
        for name,setup in self._storage.load().items():
            self._config_object[name]=Setup(setup)
    def save(self):
        if not self._storage:
            raise ConfigError("No Storage Module Loaded")
        self._storage.save(self._config_object)
    def get(self,name):
        return self._config_object[name]
    def getAll(self):
        return self._config_object
    def store(self,name,setup):
        self._config_object[name]=setup

class ConfigStore:
    def __init__(self):
        pass
    def save(self,config):
        pass
    def load(self):
        return AttrDict()

class ConfigJson(ConfigStore):
    def __init__(self,filename):
        self.filename = filename
    def load(self):
        with open(self.filename, 'r') as f:
            content = json.load(f)
        return AttrDict(content)
    def save(self,content):
        toSave = dict(content)
        saveFinal = {}
        print(toSave)
        for name,setup in toSave.items():
            saveFinal[name] = setup.__dict__
        with open(self.filename, 'w') as f:
            json.dump(saveFinal,f)

class Setup:
    def __init__(self,setup=None):
        if setup:
            self.image = setup['image']
        else:
            self.image = ""
    def __repr__(self):
        return repr(self.__dict__)
