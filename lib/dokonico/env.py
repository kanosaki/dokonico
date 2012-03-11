

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
        return """C:\Users\{0}""".format(self.username)

class _MacEnvHelper(EnvHelper):
    name = "Mac"
    @property
    def is_mac(self):
        return True

    @property
    def homedir(self):
        return "/Users/{0}".format(self.username)

class _LinuxEnvHelper(EnvHelper):
    name = "Linux"
    @property
    def is_linux(self):
        return True

    @property
    def homedir(self):
        return "/home/{0}".format(self.username)

class UnsupportedOSError(Exception):
    pass
