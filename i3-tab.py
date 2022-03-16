#!/usr/bin/env python3

import sys
import configUtils
from gui import Launcher
from wm import WindowManager

def main():
    if len(sys.argv) < 2:
        print("Please specify a config path")
        return
    
    config = configUtils.load(sys.argv[1])
    if config == None:
        return
    
    window_manager = WindowManager()
    window_manager.reload()
    Launcher(window_manager, config).main()

if __name__ == '__main__':
    main()