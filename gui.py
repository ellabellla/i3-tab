import PySimpleGUI as sg

class Launcher():
    def __init__(self, window_manager):
        self._queue = []
        self._window_manager = window_manager

        layout = [[sg.Text('hello', key='body')]]      

        self._window = sg.Window("", layout, no_titlebar=True)
        
        self._selected = 0

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
    
    def _close(self):
        self._window_manager.exit()
        self._window.close()
    
if __name__ == '__main__':
    launcher = Launcher() 
    launcher.main()