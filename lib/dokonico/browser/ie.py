
import ctypes as ct

import dokonico
import dokonico.core
from dokonico.browser import common

InternetGetCookie = ct.windll.InternetGetCookieA
InternetGetCookie.res_type = ct.wintypes.BOOL
InternetSetCookie = ct.windll.InternetSetCookieA
InternetSetCookie.res_type = ct.wintypes.BOOL

class APIError(Exception):
    pass

def _invoke_api(api, url, name):
    size = ct.wintypes.DWORD(1024)
    buf = ct.c_buffer(size.value)
    res = api(url, name, buf, ct.pointer(size))
    if res:
        return buf.value
    else:
        raise APIError()


def get_cookie(url, name):
    return _invoke_api(InternetGetCookie, url, name)

def set_cookie(url, name):
    return _invoke_api(InternetSetCookie, url, name)

class IEFactory(common.BrowserFactory):
    def windows(self):
        return IE()

    def mac(self):
        raise Exception("IE is not supported in Mac OS")


class IE(common.Browser):
    name = "IE"
    def push(self, cookie):
        pass
    
    def pull(self):
        pass

class IECookie(dokonico.core.Cookie):
    def __init__(self, dic, browser):
        self.browser_name = browser
        dokonico.core.Cookie.__init__(self, dic)
        
