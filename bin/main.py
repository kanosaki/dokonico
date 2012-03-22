
import sys
import os

if sys.version < '3':
    print("This application supports Python 3 or later.")
    sys.exit(-1)

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
LIB_DIR = os.path.join(APP_ROOT, "lib")
sys.path.insert(0, LIB_DIR)

import dokonico
import dokonico.env

if __name__ == '__main__':
    dokonico.start()
    if dokonico.env.current.promt_at_end:
        input("Press any key to exit.")
        
