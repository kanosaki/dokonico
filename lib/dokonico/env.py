

import platform
import os

class EnvHelperFactory:
    def create(self):
        os_name = platform.system()
        if os_name == "Windows":
            return _WindowsEnvHelper()
        elif os_name == "Darwin":
            return _MacEnvHelper()
        elif os_name == "Linux":
            return _LinuxEnvHelper()
        else:
            raise UnsupportedOSError()

class EnvHelper:
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
