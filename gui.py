import PySimpleGUI as sg
from pynput import keyboard

class Launcher():
    def __init__(self, window_manager):
        self._queue = []
        self._window_manager = window_manager

        layout = [[sg.Text('hello', key='body')]]      

        self._window = sg.Window("", layout, no_titlebar=True)
        
        self._selected = 0
        
        self._listener = keyboard.Listener(
            on_press=self._create_on_key_press(),
            on_release=self._create_on_key_release())
        
        self._alt_down = False
        self._hidden = True
        
        self._window_list = [];
        
        self._listener.start()

    def main(self):
        event, values = self._window.read(timeout=100) 
        self._window.hide()
        while True:
            event, values = self._window.read(timeout=100) 
            if event == sg.WIN_CLOSED or event == 'Exit':
                self._close()
                break
            else:
                self._window_list = [ (window['id'], window['name']) for window in filter(lambda window: window['name'] != None, self._window_manager._windows)]
                self._window['body'].update(' | '.join([f'_{name}_' if self._selected == i else name for i, (_, name) in enumerate(self._window_list)]))
    
    def _create_on_key_press(self):
        def _on_key_press(key):
            try:
                if self._alt_down and key.name == 'tab':
                    if self._hidden:
                        self._hidden = False
                        self._window.un_hide()
                        self._window.TKroot.focus_force()
                    else:
                        self._selected += 1
                        if self._selected >= len(self._window_list):
                            self._selected = 0
                elif key.name == 'alt':
                    self._alt_down = True
                
            except AttributeError:
                pass
            
        return _on_key_press
    
    def _create_on_key_release(self):
        def _on_key_release(key):
            try:
                if key.name == 'alt':
                    self._alt_down = False
                    if not self._hidden:
                        self._hidden = True
                        self._window.hide()
                        self._window_manager.cmd(f'[con_id="{self._window_list[self._selected][0]}"] focus')
                        self._selected = 0
            except AttributeError:
                pass
        
        return _on_key_release
    
    def _close(self):
        self._window_manager.exit()
        self._window.close()
    
if __name__ == '__main__':
    launcher = Launcher() 
    launcher.main()