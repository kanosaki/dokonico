
import json

def config_item(loc):
    def wrap(f):
        def get(self):
            try:
                return f(self)
            except KeyError:
                raise Exception("Invalid setting file, {0} was not found.".format(loc))
        return get
    return lambda s : property(wrap(s))

class Config:
    def __init__(self, path):
        self.load(path)

    def load(self, path):
        with open(path) as f:
            self.dic = json.load(f)

    @config_item("/sync_system/mode")
    def sync_mode(self):
        return self.dic["sync_system"]["mode"]
    
    @config_item("/dropbox")
    def dropbox(self):
        return self.dic["dropbox"]

    @config_item("/gdata")
    def gdata(self):
        return self.dic["gdata"]

    @config_item("/custom_server")
    def custom_server(self):
        return self.dic["custom_server"]

class Cookie:
    def __init__(self, dic):
        self.dic = dic

    def __getattr__(self, key):
        if key in self.dic:
            return self.dic[key]
        else:
            raise AttributeError()
        

