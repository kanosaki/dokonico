
class Firefox:
    pass


class FirefoxFactory:
    def windows(self):
        return FirefoxWin()

    def mac(self):
        return FirefoxMac()

class FirefoxWin(Firefox):
    pass

class FirefoxMac(Firefox):
    pass

