# coding=utf-8
import wx


class ContentFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None):
        wx.Frame.__init__(self, parent, -1, title='天马行空的朋友圈', size=(400, 400), pos=(500, 200))

        self.UpdateUI = UpdateUI
        self.InitUI()  # 绘制UI

    def InitUI(self):
        panel = wx.Panel(self)
        wx.StaticText(panel, -1, u'欢迎您的到来!', pos=(30, 30))
