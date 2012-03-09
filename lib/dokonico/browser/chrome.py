

class Chrome:
    pass

class ChromeFactory:
    def windows(self):
        return ChromeWin()

    def mac(self):
        return ChromeMac()

class ChromeWin(Chrome):
    @property
    def cookie_db_file(self):
        return """C:\<<UserName>>\Local\Google\Chrome\Default\User Data\Cookies"""


class ChromeMac(Chrome):
    @property
    def cookie_db_file(self):
        return """/Users/<<UserName>>/Library/Application Support/Google/Chrome/Default/Cookies"""
