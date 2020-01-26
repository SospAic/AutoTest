# coding=utf-8
import wx
# 导入wxPython中的通用Button
import wx.lib.buttons as wxButton
import wxPythonSimple.wxPyFrame.xDialog
from wxPythonSimple.wxPyFrame.utils import load_image


class LoginFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None):
        wx.Frame.__init__(self, parent, id, title='登录界面', size=(280, 400), pos=(500, 200))

        self.UpdateUI = UpdateUI
        self.InitUI()  # 绘制UI界面

    def InitUI(self):
        panel = wx.Panel(self)

        logo_sys = wx.Image(load_image('logo_sys.png'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(panel, -1, logo_sys, pos=(90, 90), size=(100, 100))

        logo_title = wx.StaticText(panel, -1, '天马行空', pos=(120, 210))
        logo_title.SetForegroundColour('#0a74f7')
        titleFont = wx.Font(13, wx.DEFAULT, wx.BOLD, wx.NORMAL, True)
        logo_title.SetFont(titleFont)

        button_Login = wxButton.GenButton(panel, -1, '登录', pos=(40, 270), size=(200, 40), style=wx.BORDER_MASK)
        button_Login.SetBackgroundColour('#0a74f7')
        button_Login.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.loginSys, button_Login)

    def loginSys(self, event):
        dlg = LoginDialog(self.loginFunction, '#0a74f7')
        dlg.Show()

    def loginFunction(self, account, password):
        print('接收到用户的输入：', account, password)
        self.UpdateUI(1)  # 更新UI-Frame


class LoginDialog(wxPythonSimple.wxPyFrame.xDialog.InputDialog):
    def __init__(self, func_callBack, themeColor):
        wxPythonSimple.wxPyFrame.xDialog.InputDialog.__init__(self, '登录系统', func_callBack, themeColor)
