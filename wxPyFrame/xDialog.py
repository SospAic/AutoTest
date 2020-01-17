# coding=utf-8

import wx


class InputDialog(wx.Dialog):
    def __init__(self, title, func_callBack, themeColor):
        wx.Dialog.__init__(self, None, -1, title, size=(300, 200))
        self.func_callBack = func_callBack
        self.themeColor = themeColor

        self.InitUI()  # 绘制Dialog的界面

    def InitUI(self):
        panel = wx.Panel(self)

        font = wx.Font(14, wx.DEFAULT, wx.BOLD, wx.NORMAL, True)

        accountLabel = wx.StaticText(panel, -1, '账号', pos=(20, 25))
        accountLabel.SetForegroundColour(self.themeColor)
        accountLabel.SetFont(font)

        self.accountInput = wx.TextCtrl(panel, -1, u'', pos=(80, 25), size=(180, -1))
        self.accountInput.SetForegroundColour('gray')
        self.accountInput.SetFont(font)

        passwordLabel = wx.StaticText(panel, -1, '密码', pos=(20, 70))
        passwordLabel.SetFont(font)
        passwordLabel.SetForegroundColour(self.themeColor)

        self.passwordInput = wx.TextCtrl(panel, -1, u'', pos=(80, 70), size=(180, -1), style=wx.TE_PASSWORD)
        self.passwordInput.SetForegroundColour(self.themeColor)
        self.passwordInput.SetFont(font)

        sureButton = wx.Button(panel, -1, u'登录', pos=(20, 130), size=(120, 40))
        sureButton.SetForegroundColour('white')
        sureButton.SetBackgroundColour(self.themeColor)
        # 为【确定Button】绑定事件
        self.Bind(wx.EVT_BUTTON, self.sureEvent, sureButton)

        cancleButton = wx.Button(panel, -1, u'取消', pos=(160, 130), size=(120, 40))
        cancleButton.SetBackgroundColour('black')
        cancleButton.SetForegroundColour('#ffffff')
        # 为【取消Button】绑定事件
        self.Bind(wx.EVT_BUTTON, self.cancleEvent, cancleButton)

    def sureEvent(self, event):
        account = self.accountInput.GetValue()
        password = self.passwordInput.GetValue()
        # 通过回调函数传递数值
        self.func_callBack(account, password)
        self.Destroy()  # 销毁隐藏Dialog

    def cancleEvent(self, event):
        self.Destroy()  # 销毁隐藏Dialog
