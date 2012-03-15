


def start():
    app = _init_app()
    app.start()

def _init_app():
    from dokonico import loader
    ldr = loader.AppLoader()
    return ldr.load()
    

    
