from turtle import pos
import wx
import wx.richtext
class Launcher(wx.Frame):
    def __init__(self, window_manager):
        self._queue = []
        self._window_manager = window_manager
        self._app = wx.App()
    
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.NO_BORDER | wx.FRAME_SHAPED  )
        super(Launcher, self).__init__(None, title='Launcher', style=style)
        
        self._panel = wx.Panel(self)
        #self._quote = wx.StaticText(self._panel, label="Your quote: ", pos=(0, 0))
        self._rtext = wx.richtext.RichTextCtrl(self._panel, size=self.Size, pos=(0,0), style=wx.richtext.RE_READONLY)
        self._rtext.Disable()
        self._rtext.SetEditable(False)
        self._rtext.WriteText("normal text")
        self._rtext.Newline()
        
        self.Show()
        
        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._update, self._timer)
        self._timer.Start(300)
        
        self.Bind(wx.EVT_CLOSE, self._close, self)
        
        self._app.MainLoop()
    
    def _update(self, event):
        self._rtext.Clear()
        self._rtext.WriteText(repr(list(self._window_manager._windows)))
        
    def _close(self, event):
        self._window_manager.exit()
        self.Destroy()
    