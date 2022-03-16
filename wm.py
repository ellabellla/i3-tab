from i3ipc import Connection, Event
from threading import Lock, Thread

class WindowManager():
    def __init__(self, testing=False):
        """Manages the state changes of i3 and keeps a list of open in windows. Switching focus will shift windows the front of the list.

        Args:
            testing (bool, optional): Disable the connection to i3 for testing. Defaults to False.
        """
        self._windows = []
        self._lock = Lock()
        
        if testing:
            self._testing = True
            return
        else:
            self._testing = False
            
        self._i3 = Connection(auto_reconnect=True)
        
        self._i3.on(Event.WINDOW_FOCUS, self._create_on_window_focus())
        self._i3.on(Event.WINDOW_NEW, self._create_on_window_new())
        self._i3.on(Event.WINDOW_CLOSE, self._create_on_window_close())
        
        self._thread = Thread(target=self._i3.main)
        self._thread.start()

    def front(self) -> dict:
        """Get the front of the window list.
        """         
        self._lock.acquire()
        front = None
        try:
            front = None if len(self._windows) == 0 else self._windows[0]
        finally:
            self._lock.release()
            return front

    def remove_window(self, id) -> None:
        """Remove window by id

        Args:
            id (string): id of window
        """
        self._lock.acquire()
        try:
            self._windows = list(filter(lambda window: window['id'] != id, self._windows))
        finally:
            self._lock.release()

    def add_window(self, id, name) -> None:
        """Add a window to the window list.

        Args:
            id (string): id of the window
            name (string): name of the window
        """
        self._lock.acquire()
        try:
            self._windows = [{'id': id, 'name': name}] + self._windows
        finally:
            self._lock.release()

    def move_to_front(self, id) -> None:
        """Move window with id to the front of the list.

        Args:
            id (string): id of the window
        """
        self._lock.acquire()
        try:
            window  = list(filter(lambda window: window['id'] == id, self._windows))
            
            if len(window) == 0:
                return
            
            self._windows = window + list(filter(lambda window: window['id'] != id, self._windows))
        finally:
            self._lock.release()
            
    def flip(self) -> None:
        """Flip the order of the first two windows in the list
        """
        if len(self._windows) < 2:
            return    
        
        self._lock.acquire()
        try:
            self._windows = [self._windows[1]] + [self._windows[0]] + self._windows[2:]
        finally:
            self._lock.release()
    
    def cmd(self, cmd) -> None:
        """Run i3 command

        Args:
            cmd (string): i3 command
        """
        tmp =self._i3.command(cmd)
    
    def reload(self) -> None:
        """Reload all window data
        """
        self._windows = []
        cons = self._i3.get_tree().leaves()
        while len(cons) != 0:
            con = cons[0]
            cons = cons[1:]
            self._windows.append({'id': con.id, 'name': con.name})
        
        self.move_to_front(self._i3.get_tree().find_focused().id)
    
    def reload_names(self)  -> None:
        """Reload the names of the windows in the window list
        """
        self._windows = [{'id': window['id'], 'name': self._i3.get_tree().find_by_id(window['id']).name} for window in self._windows] 

    def exit(self) -> None:
        """Exit i3 loop and close thread.
        """
        self._i3.main_quit()
        self._thread.join()
        
    def _create_on_window_focus(self):
        """Create on window focus event handler
        """
        def closure(connection, e):
            self.move_to_front(e.container.id)
        
        return closure
    
    def _create_on_window_new(self):
        """Create on window new event handler
        """
        def closure(connection, e):
            self.add_window(e.container.id, e.container.name)
        
        return closure

    def _create_on_window_close(self):
        """Create on window close event handler
        """
        def closure(connection, e):
            self.remove_window(e.container.id)
        
        return closure