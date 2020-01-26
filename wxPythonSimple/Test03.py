import logging
import random
import sys
import wx

logger = logging.getLogger(__name__)


class WxTextCtrlHandler(logging.Handler):
    def __init__(self, ctrl):
        logging.Handler.__init__(self)
        self.ctrl = ctrl

    def emit(self, record):
        s = self.format(record) + '\n'
        wx.CallAfter(self.ctrl.WriteText, s)


LEVELS = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]


class Frame(wx.Frame):
    def __init__(self):
        TITLE = "wxPython Logging To A Control"
        wx.Frame.__init__(self, None, wx.ID_ANY, TITLE)
        panel = wx.Panel(self, wx.ID_ANY)
        log = wx.TextCtrl(panel, wx.ID_ANY, size=(300, 100),
                          style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        btn = wx.Button(panel, wx.ID_ANY, 'Log something!')
        self.Bind(wx.EVT_BUTTON, self.onButton, btn)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(log, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)
        handler = WxTextCtrlHandler(log)
        logger.addHandler(handler)
        FORMAT = "%(asctime)s %(levelname)s %(message)s"
        handler.setFormatter(logging.Formatter(FORMAT))
        logger.setLevel(logging.DEBUG)

    def onButton(self, event):
        logger.log(random.choice(LEVELS), "More? click again!")


if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = Frame().Show()
    app.MainLoop()
