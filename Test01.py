import wx
import sys


class Frame(wx.Frame):
    def __init__(self, parent, id, title):
        print("frame init ...")
        wx.Frame.__init__(self, parent, id, title)


class App(wx.App):
    def __init__(self, redirect=True, filename=None):
        print("App init...")
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        print("oninit...")
        self.frame = Frame(parent=None, id=-1, title='hello')
        self.frame.Show()
        self.SetTopWindow(self.frame)
        print(sys.stderr, "error message")
        return True

    def OnExit(self):
        print("OnExit")


if __name__ == '__main__':
    app = App(redirect=True)
    print("begin mainloop")
    app.MainLoop()
    print("end mainloop")
