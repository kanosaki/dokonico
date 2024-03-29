
import datetime
import json
import socket
import os

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

JST_DELTA = datetime.timedelta(hours=9)

class Cookie:
    def __init__(self, dic):
        self.dic = dic
        self.set_identifier()

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getattr__(self, key):
        if key in self.dic:
            return self.dic[key]
        else:
            raise AttributeError()

    def __lt__(self, other):
        return self.creation_ticks < other.creation_ticks

    def __eq__(self, other):
        return self.creation_ticks == other.creation_ticks

    def set_identifier(self):
        i = "{}[{}@{}]".format(self.browser_name, os.getlogin(), socket.gethostname())
        self.identifier = i

    def is_newer_than(self, that):
        return self > that

    def __repr__(self):
        com_cookie = self.to_common()
        return """Session [Created {}]""".format(
                self._repr_utc_time(com_cookie["creation_utc"]))

    def _repr_utc_time(self, time):
        t = datetime.datetime.utcfromtimestamp(time / 1000000)
        return (t + JST_DELTA).strftime("%Y/%m/%d(%a) %H:%M:%S")
    
    def to_common(self):
        return self.dic
        

