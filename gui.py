from math import floor
import PySimpleGUI as sg
from pynput import keyboard

class Launcher():
    def __init__(self, window_manager, config):
        """Alt Tab Menu GUI. Handles all keyboard interactions and gui.

        Args:
            window_manager (WindowManager): i3 WindowManager
        """
        self._queue = []
        self._config = config
        self._window_manager = window_manager

        layout = [[sg.Text('', key=str(i), text_color=config['window']['color'], background_color=config['window']['bcolor'], 
                           size=(config['selection']['width'], config['selection']['height']), 
                           font=config['font']['unselected']) for i in range(0,self._config['window'].getint('width'))]]      

        self._window = sg.Window("i3-tab", layout, background_color=config['window']['bcolor'])
        
        self._selected = 0
        
        self._listener = keyboard.Listener(
            on_press=self._create_on_key_press(),
            on_release=self._create_on_key_release())
        
        self._alt_down = False
        self._shift_down = False
        self._hidden = True
        
        self._window_list = [];
        
        self._listener.start()

    def main(self) -> None:
        """Start main gui loop.
        """
        event, values = self._window.read(timeout=100) 
        self._window.hide()
        self._window_manager.reload()
        while True:
            event, values = self._window.read(timeout=100) 
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                self._close()
                break
            else:
                for i in range(0,self._config['window'].getint('width')):
                    index = i
                    index += floor(self._selected / self._config['window'].getint('width')) * self._config['window'].getint('width')
                        
                    if index >= len(self._window_list):
                        self._window[str(i)].update('')
                        continue
                    
                    self._window[str(i)].update(self._window_list[index][1], 
                                                font=(self._config['font']['selected'] if self._selected == index else self._config['font']['unselected']))
    
    def _create_on_key_press(self):
        """Create on key press event handler
        """
        def _on_key_press(key):
            try:
                if self._alt_down and key.name == 'tab':
                    if self._hidden:
                        self._hidden = False
                        self._window_manager.reload_names()
                        self._window_list = [ (window['id'], window['name']) for window in filter(lambda window: window['name'] != None, self._window_manager._windows)]
                        
                        self._window_manager.cmd('fullscreen disable')
                        self._window.un_hide()
                        self._window.TKroot.focus_force()
                    
                    self._selected += 1    
                    if self._selected >= len(self._window_list):
                        self._selected = 0
                elif key.name == 'alt':
                    self._alt_down = True
                elif self._alt_down and key.name == 'shift':
                    self._selected -= 1
                    if self._selected < 0:
                        self._selected = len(self._window_list) - 1
                
            except AttributeError:
                pass
            
        return _on_key_press
    
    def _create_on_key_release(self):
        """Create on key release event handler
        """
        def _on_key_release(key):
            try:
                if key.name == 'alt':
                    self._alt_down = False
                    if not self._hidden:
                        self._hidden = True
                        self._window.hide()
                        self._window_manager.cmd(f'[con_id="{self._window_list[self._selected][0]}"] focus')
                        self._selected = 0
                if key.name == 'shift':
                    self._shift_down = False
            except AttributeError:
                pass
        
        return _on_key_release
    
    def _close(self):
        """Exit window manager and close Gui.
        """
        self._window_manager.exit()
        self._window.close()