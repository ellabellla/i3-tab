from i3ipc import Connection, Event
from threading import Lock, Thread
from itertools import chain

class WindowManager():
    def __init__(self, testing=False):
        self._windows = []
        self._lock = Lock()
        
        if testing:
            self._testing = True
            return
        else:
            self._testing = False
            
        self._i3 = Connection(auto_reconnect=True)
        
        self._i3.on(Event.WINDOW_NEW, self._create_on_window_new())
        self._i3.on(Event.WINDOW_CLOSE, self._create_on_window_close())
        
        self._thread = Thread(target=self._i3.main)
        self._thread.start()

    def front(self):            
        self._lock.acquire()
        front = None
        try:
            front = None if len(self._windows) == 0 else self._windows[0]
        finally:
            self._lock.release()
            return front

    def remove_window(self, id):
        self._lock.acquire()
        try:
            self._windows = list(filter(lambda window: window['id'] != id, self._windows))
        finally:
            self._lock.release()

    def add_window(self, id, name):
        self._lock.acquire()
        try:
            self._windows = [{'id': id, 'name': name}] + self._windows
        finally:
            self._lock.release()

    def move_to_front(self, id):
        self._lock.acquire()
        try:
            window  = list(filter(lambda window: window['id'] == id, self._windows))
            
            if len(window) == 0:
                return
            
            self._windows = window + list(filter(lambda window: window['id'] != id, self._windows))
        finally:
            self._lock.release()
            
    def flip(self):
        if len(self._windows) < 2:
            return    
        
        self._lock.acquire()
        try:
            self._windows = [self._windows[1]] + [self._windows[0]] + self._windows[2:]
        finally:
            self._lock.release()

    def _create_on_window_new(self):
        def closure(connection, e):
            self.add_window(e.container.id, e.container.name)
        
        return closure

    def _create_on_window_close(self):
        def closure(connection, e):
            self.remove_window(e.container.id)
        
        return closure