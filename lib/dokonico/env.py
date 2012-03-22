

import platform
import os

current = None

def init(opts):
    global current
    factory = EnvHelperFactory(opts)
    current = factory.create()

class EnvHelperFactory:
    def __init__(self, opts):
        self.opts = opts
        
    def create(self):
        os_name = platform.system()
        if os_name == "Windows":
            return _WindowsEnvHelper(self.opts)
        elif os_name == "Darwin":
            return _MacEnvHelper(self.opts)
        elif os_name == "Linux":
            return _LinuxEnvHelper(self.opts)
        else:
            raise UnsupportedOSError()

class EnvHelper:
    def __init__(self, opts):
        self.opts = opts
        
    @property
    def is_windows(self):
        return False

    @property
    def is_mac(self):
        return False

    @property
    def is_linux(self):
        return False

    @property
    def username(self):
        return os.getlogin()
    
    @property
    def promt_at_end(self):
        return self.is_windows and not self.opts.from_gui

class _WindowsEnvHelper(EnvHelper):
    name = "Windows"
    @property
    def is_windows(self):
        return True

    @property
    def homedir(self):
        return os.environ['USERPROFILE']

    @property
    def app_data(self):
        return os.environ['APPDATA']

class _UnixEnvHelper(EnvHelper):
    name = "Unix"
    @property
    def homedir(self):
        return os.environ['HOME']

class _MacEnvHelper(_UnixEnvHelper):
    name = "Mac"
    @property
    def is_mac(self):
        return True

class _LinuxEnvHelper(_UnixEnvHelper):
    name = "Linux"
    @property
    def is_linux(self):
        return True

class UnsupportedOSError(Exception):
    pass

