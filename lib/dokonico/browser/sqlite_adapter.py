
import sqlite3
import os
import json

def cached_property(f):
    """returns a cached property that is calculated by function f"""
    def get(self):
        try:
            return self._property_cache[f]
        except AttributeError:
            self._property_cache = {}
            x = self._property_cache[f] = f(self)
            return x
        except KeyError:
            x = self._property_cache[f] = f(self)
            return x
    return property(get)

class SQLiteAdapter:
    def __init__(self, file_path, browser_name):
        self.path = file_path
        self.browser_name = browser_name

    def connect(self):
        self.connection = sqlite3.connect(self.path)

    def close(self):
        self.connection.close()

    def _execute_sql(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def query(self):
        sql = self.name_table.select_query
        return list(map(self.name_table.create_dict,
                self._execute_sql(sql)))

    @cached_property
    def name_table(self):
        factory = NameTableFactory.default
        return factory.create(self.browser_name)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
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

    @property
    def common_names(self):
        return [ c[1] for c in self._cols ]

    def special_name(self, name):
        """Converts common column name to browser specific column name."""
        return self._from_common_name(name)
    
    def _from_common_name(self, cname):
        for (k,v) in self._cols:
            if v == cname:
                return k
        raise KeyError("Key [{0}] was not found.".format(cname))
    
    def create_dict(self, values):
        return dict(zip(self.common_names, values))

    @property
    def _cols(self):
        return self.data["columns"]
    
    @property
    def target_table(self):
        return self.data["table_name"]

    @property
    def where_pred(self):
        return "{0} = '{1}' and {2} = '{3}'".format(
                self.special_name("host_key"), self.whole["host_key"],
                self.special_name("name"), self.whole["session_cookie"])
    
    @property
    def select_query(self):
        return """
            SELECT {0} FROM {1} WHERE {2}
        """.format(
                ",".join(self.column_headers),
                self.target_table,
                self.where_pred)

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
        
