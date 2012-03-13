
import datetime
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

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getattr__(self, key):
        if key in self.dic:
            return self.dic[key]
        else:
            raise AttributeError()

    def is_newer_than(self, cookie):
        this_created = self.time_comparator
        that_created = cookie.time_comparator
        return this_created > that_created

    @property
    def last_access_ticks(self):
        return int(self.last_access_utc)

    def __repr__(self):
        return """Found! [Last accessed {}, Expires {}]""".format(
                self._repr_utc_time(self.last_access_ticks),
                self._repr_utc_time(self.expires_utc))

    def _repr_utc_time(self, time):
        t = datetime.datetime.utcfromtimestamp(time)
        return t.strftime("%Y/%m/%d(%a) %H:%M:%S")

