
class RemoteManager:
    def __init__(self, env, conf):
        self.env = env
        self.conf = conf
        
    def pull(self):
        return self.current.pull()

    def push(self, cookie):
        self.current.push(cookie)
    
    @property
    def current(self):
        try:
            return self._current
        except AttributeError:
            self._current = self.create_remote()
            return self._current
    
    def create_remote(self):
        mode = self.conf.sync_mode
        if mode == "Dropbox":
            from dokonico.remote import dropbox
            return dropbox.Dropbox(env, conf)
        else:
            raise Exception("Unsupported sync_mode {0}".format(mode))
