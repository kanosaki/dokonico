
import sys
import os

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
LIB_DIR = os.path.join(APP_ROOT, "lib")
sys.path.insert(0, LIB_DIR)

import dokonico

if __name__ == '__main__':
    dokonico.start()
