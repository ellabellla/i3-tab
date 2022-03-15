from gui import Launcher
from wm import WindowManager

def main():
    window_manager = WindowManager()
    Launcher(window_manager)

if __name__ == '__main__':
    main()