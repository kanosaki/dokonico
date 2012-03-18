
import sqlite3
import os
import json
import logging as log

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
        #self.connection.row_factory = sqlite3.Row

    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def execute_sql(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        cursor.close()
        return ret

    def query(self):
        sql = self.query_builder.select()
        log.info("SELECT Query to {}: {}".format(self.browser_name, sql))
        return list(map(self.query_builder.create_dict,
                self.execute_sql(sql)))

    def update(self, dic):
        sql = self.query_builder.update(dic)
        log.info("UPDATE Query to {}: {}".format(self.browser_name, sql))
        self.execute_sql(sql)

    def insert(self, dic):
        sql = self.query_builder.insert(dic)
        log.info("INSERT Query to {}: {}".format(self.browser_name, sql))
        self.execute_sql(sql)

    @cached_property
    def query_builder(self):
        factory = QueryBuilderFactory(self)
        return factory.create(self.browser_name)
    
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is None:
            self.commit()
        self.close()

class QueryBuilderFactory:
    def __init__(self, adapter):
        self.adapter = adapter
        p = os.path
        self.table_path = p.abspath(p.join(p.dirname(__file__), "./table.json")) 
        self.load()

    def load(self):
        with open(self.table_path) as f:
            self.data = json.load(f)

    def create(self, browser_name):
        if browser_name == "Chrome":
            return ChromeQueryBuilder(self.adapter)
        elif browser_name == "Firefox":
            return FirefoxQueryBuilder(self.adapter)
        else:
            raise ValueError("Unsupported browser!")


class QueryBuilder:
    def __init__(self, adapter):
        self.adapter = adapter
        self.names = self.create_name_table()

    def select(self):
        return """SELECT {0} FROM {1} WHERE {2};""".format(
                ",".join(self.names.column_headers),
                self.names.target_table,
                self.names.where_pred)

    def update(self, dic):
        return """UPDATE {0} SET {1} WHERE {2};""".format(
                self.names.target_table,
                self.update_pairs(dic),
                self.names.where_pred)

    def insert(self, dic):
        return """INSERT INTO {0} VALUES({1})""".format(
                self.names.target_table,
                self.insert_tuple_expr(dic))

    def insert_tuple_expr(self, dic):
        return ",".join(
                [ self.value_expr(dic,h) for h in self.names.column_headers ])

    def value_expr(self, dic, name):
        cname = self.names.common_name(name)
        return self.expr_by_type(cname, dic[cname])

    def expr_by_type(self, cname, value):
        val_type = self.names.common_type(cname)
        if val_type == "str":
            return "'{0}'".format(value)
        elif val_type == "int":
            return value
        else:
            raise Exception("Invalid column type: {0} at table definition".format(val_type))

    def update_pairs(self, dic):
        ret = []
        for header in self.names.column_headers:
            cname = self.names.common_name(header)
            try:
                value = dic[cname] 
            except KeyError:
                value = self.names.default_value(cname)
            expr = "{0}={1}".format(header, self.expr_by_type(cname, value))
            ret.append(expr)
        return ",".join(ret)
    

    def create_dict(self, values):
        return dict(zip(self.names.common_names, values))

class ChromeQueryBuilder(QueryBuilder):
    def create_name_table(self):
        factory = NameTableFactory()
        return factory.create("Chrome")
        

class FirefoxQueryBuilder(QueryBuilder):
    def create_name_table(self):
        factory = NameTableFactory()
        return factory.create("Firefox")

    def insert_tuple_expr(self, dic):
        dic["id"] = str(self.next_id())
        return ",".join(
                [ self.value_expr(dic,h) for h in self.names.column_headers ])
    
    def next_id(self):
        a = self.adapter
        sql = "SELECT MAX(id) FROM moz_cookies;"
        return a.execute_sql(sql)[0][0] + 1

class NameTableFactory:
    def __init__(self):
        p = os.path
        self.path = p.abspath(p.join(p.dirname(__file__), "./table.json")) 
        self.load()

    def load(self):
        with open(self.path) as f:
            self.data = json.load(f)

    def create(self, name):
        if name == "Chrome":
            return _ChromeNameTable(self.data)
        elif name == "Firefox":
            return _FirefoxNameTable(self.data)
        else:
            raise ValueError("Unsupported browser!")

class NameTable:
    def initialize(self):
        self.data = self.whole[self.name]

    def default_value(self, cname):
        return self.whole["default_values"][cname]

    def common_name(self, sname):
        """Converts browser specific column name to common column name."""
        for (k,v) in self._cols:
            if k == sname:
                return v
        raise KeyError("Key [{0}] was not found.".format(sname))

    def common_type(self, cname):
        return self.whole["types"][cname]
    
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

NameTableFactory.default = NameTableFactory()
    
class _ChromeNameTable(NameTable):
    name = "Chrome"
    def __init__(self, data):
        self.whole = data
        self.initialize()

class _FirefoxNameTable(NameTable):
    name = "Firefox"
    def __init__(self, data):
        self.whole = data
        self.initialize()
        
