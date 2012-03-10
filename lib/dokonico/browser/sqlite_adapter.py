
import sqlite3
import os
import json

class SQLiteAdapter:
    def __init__(self, file_path, browser_name):
        self.path = file_path
        self.browser_name = browser_name

    def connect(self):
        self.connection = sqlite3.connect(self.path)

    def close(self):
        self.connection.close()

    def query(self, pred):
        pass

    def __enter__(self):
        self.connect()

    def __exit__(self):
        self.close()

class NameTableFactory:
    def __init__(self):
        p = os.path
        self.path = p.abspath(p.join(p.dirname(__file__), "./table.json")) 
        self.load()

    def load(self):
        with open(self.path) as f:
            self.data = json.load(f)

    def create(self, name):
        if name == "chrome":
            return _ChromeNameTable(self.data)
        elif name == "firefox":
            return _FirefoxNameTable(self.data)
        else:
            raise ValueError("Unsupported browser!")

# Default instance
NameTableFactory.default = NameTableFactory()
        
class NameTable:
    def initialize(self):
        self.data = self.whole[self.name]

    def common_name(self, sname):
        """Converts browser specific column name to common column name."""
        for (k,v) in self._cols:
            if k == sname:
                return v
        raise KeyError("Key [{0}] was not found.".format(sname))
    
    def column_number(self, name):
        i = 0
        for (k,v) in self._cols:
            if k == name:
                return i
            i += 1

    @property
    def column_headers(self):
        return [ c[0] for c in self._cols ]

    def special_name(self, name):
        """Converts common column name to browser specific column name."""
        return self._from_common_name(name)
    
    def _from_common_name(self, cname):
        for (k,v) in self._cols:
            if v == cname:
                return k
        raise KeyError("Key [{0}] was not found.".format(cname))

    @property
    def _cols(self):
        return self.data["columns"]
        

class _ChromeNameTable(NameTable):
    name = "chrome"
    def __init__(self, data):
        self.whole = data
        self.initialize()

class _FirefoxNameTable(NameTable):
    name = "firefox"
    def __init__(self, data):
        self.whole = data
        self.initialize()
        
