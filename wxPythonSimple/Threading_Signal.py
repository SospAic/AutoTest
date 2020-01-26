import time
import wx
from threading import Thread
from wx.lib.pubsub import pub

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()


def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


class WorkerThread(Thread):
    def __init__(self, notify_window):
        # 线程实例化时立即启动
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.start()

    def run(self):
        # 线程执行的代码
        for i in range(101):
            time.sleep(0.03)
            wx.CallAfter(pub.sendMessage, "update", msg=i)
            time.sleep(0.5)
            if self._want_abort:
                # Use a result of None to acknowledge the abort (of
                # course you can use whatever you'd like or even
                # a separate event type)
                wx.PostEvent(self._notify_window, ResultEvent(None))
                return
        # Here's where the result would be returned (this is an
        # example fixed result of the number 10, but it could be
        # any Python object)
        wx.PostEvent(self._notify_window, ResultEvent(10))

    def abort(self):
        self._want_abort = 1


class MyForm(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="线程信号测试", pos=wx.DefaultPosition,
                          size=wx.Size(-1, -1), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        gSizer2 = wx.GridSizer(0, 4, 0, 0)
        self.m_button2 = wx.Button(self, wx.ID_ANY, "执行线程", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer2.Add(self.m_button2, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.m_button3 = wx.Button(self, ID_STOP, 'Stop', pos=(0, 50))
        gSizer2.Add(self.m_button3, 0, wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, "MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        gSizer2.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.m_gauge1 = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.m_gauge1.SetValue(0)
        gSizer2.Add(self.m_gauge1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(gSizer2)
        self.Layout()
        gSizer2.Fit(self)
        self.Centre(wx.BOTH)
        self.m_button2.Bind(wx.EVT_BUTTON, self.onButton)
        pub.subscribe(self.updateDisplay, "update")
        self.status = wx.StaticText(self, -1, '', pos=(0, 100))
        self.Bind(wx.EVT_BUTTON, self.OnStop, id=ID_STOP)
        EVT_RESULT(self, self.OnResult)
        self.worker = None

    def updateDisplay(self, msg):
        t = msg
        if isinstance(t, int):  # 如果是数字，说明线程正在执行，显示数字
            self.m_staticText2.SetLabel("%s%%" % t)
            self.m_gauge1.SetValue(t)
        else:  # 否则线程未执行，将按钮重新开启
            self.m_staticText2.SetLabel("%s" % t)
            self.m_button2.Enable()

    def onButton(self, event):
        if not self.worker:
            self.m_staticText2.SetLabel("线程开始")
            self.worker = WorkerThread(self)
            event.GetEventObject().Disable()

    def OnStop(self, event):
        if self.worker:
            self.m_staticText2.SetLabel("正在终止")
            self.worker.abort()

    def OnResult(self, event):
        if event.data is None:
            self.m_staticText2.SetLabel('运行终止')
        else:
            # Process results here
            self.m_staticText2.SetLabel('运行结果: %s' % event.data)
        # In either event, the worker is done
        self.worker = None
        self.m_button2.Enable()


if __name__ == "__main__":
    app = wx.App()
    MyForm(None).Show()
    app.MainLoop()
