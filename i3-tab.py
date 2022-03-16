from gui import Launcher
from wm import WindowManager

def main():
    window_manager = WindowManager()
    window_manager.reload()
    Launcher(window_manager).main()

if __name__ == '__main__':
    main()