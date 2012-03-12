

DEFAULT_CONF_PATH = "etc/config.json"

def start(options = {}):
    conf_path = options.get("conf_path") or DEFAULT_CONF_PATH
    start_sync(conf_path)

def _init_app(conf_path):
    from dokonico import loader
    ldr = loader.AppLoader(conf_path)
    return ldr.load()
    

def start_sync(conf_path):
    app = _init_app()
    app.sync_latest()

def show_sessions(conf_path):
    pass
    
