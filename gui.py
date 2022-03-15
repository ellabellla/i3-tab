import wx
class Launcher(wx.Frame):
    def __init__(self, window_manager):
        self._queue = []
        self._window_manager = window_manager
        self._app = wx.App()
    
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.NO_BORDER | wx.FRAME_SHAPED  )
        super(Launcher, self).__init__(None, title='Launcher', style=style)
        
        self._panel = wx.Panel(self)
        self._quote = wx.StaticText(self._panel, label="Your quote: ", pos=(0, 0))
        
        self.Show(True)
        
        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._update, self._timer)
        self._timer.Start(300)
        
        self._app.MainLoop()
    
    def _update(self, event):
        self._quote.LabelText = repr(list(self._window_manager._windows))
    