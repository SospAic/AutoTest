import logging
import os
import sys
import time
import traceback

import wx.lib.newevent
import wx


class App(wx.App):
    def OnInit(self):
        main_window = MainWindow(None, title='批处理图形化界面')
        main_window.Show()
        # self.SetTopWindow(main_window)
        return True


class MainWindow(wx.Frame):
    def __init__(self, *args, size=(800, 600), **kwargs):
        super().__init__(*args, size=size, **kwargs)
        self.SetMaxSize((800, 600))
        self.SetMinSize((800, 600))
        self.create_widgets()
        self.Bind(wx.EVT_LISTBOX, self._get_dir_elements, self.listBox)
        self.Bind(wx.EVT_CHOICE, self._get_dir, self.menu_select)
        self.Bind(wx.EVT_BUTTON, self._submit_event, self.submit_button)
        self.Bind(wx.EVT_BUTTON, self.pg_exit, self.exit_button)
        # self.Bind(wx.EVT_MENU, self.menu_handler)  # 第二种事件绑定方式
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)

    def OnEnterWindow(self, event):
        print("鼠标进入")
        self.SetStatusText("鼠标进入")

    def create_widgets(self):
        self._create_menubar()
        self.CreateStatusBar()
        self.control_window()
        self._console_log()

    def control_window(self):
        self.panel = wx.Panel(self, -1)
        self.menu_select = wx.Choice(self.panel, -1, pos=(20, 15), size=(200, 160), choices=index_list, style=0,
                                     validator=wx.DefaultValidator, name="choice")
        self.check_list = []
        self.listBox = wx.ListBox(self.panel, -1, (20, 50), (200, 400), self.check_list, wx.LB_MULTIPLE,
                                  validator=wx.DefaultValidator, )
        self.listText = wx.StaticText(self.panel, -1, '示例文本', (240, 20), (200, 15), style=0, name="staticText")
        self.listText.SetLabelText('Hello World')
        indexFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=False, faceName="",
                            encoding=wx.FONTENCODING_DEFAULT)
        self.submit_button = wx.Button(self.panel, -1, u"确定", (20, 460), size=wx.DefaultSize, style=0)
        self.exit_button = wx.Button(self.panel, -1, u"退出", (130, 460), size=wx.DefaultSize, style=0)

    def _get_dir_elements(self, event):
        self.listBox = event.GetEventObject()
        # print("选择{0}".format(self.listBox.GetSelections()))

    def _get_dir(self, event):
        self.menu_select = event.GetEventObject()
        select_num = self.menu_select.GetSelection()
        self.select_dir = index_list[select_num]
        # print(self.select_dir)
        if select_num > -1:
            os.chdir('./{}'.format(index_list[select_num]))
            dirs = os.listdir('./')
            file_list = []
            for i in dirs:  # 循环读取路径下的文件并筛选输出
                if os.path.splitext(i)[1] == ".py":  # 筛选执行文件
                    file_list.append(i[:-3])
                    # print(i)
            # print(file_list)
            self.check_list = file_list
            self.listBox.Set(self.check_list)
            os.chdir('../')
            # print("选择{0}".format(self.menu_select.GetSelection()))
        else:
            print('索引值错误')
            pass

    def _create_menubar(self):
        menubar = wx.MenuBar()
        menus = {
            '文件': (
                (wx.ID_SAVEAS, '导出运行结果..\tCtrl+E', '将运行结果导出至文本文件', self.file_export, 1),
                (wx.ID_CLOSE, '退出\tCtrl+Q', '退出程序', self.pg_exit, 2),
            ),
            '其他': (
                (wx.ID_ABOUT, '关于', '关于软件', self._menu_about, 2),
            )
        }
        for title, items in menus.items():
            menu = wx.Menu()
            for id_, label, help_string, handler, num in items:
                item = menu.Append(id_, label, help_string, kind=wx.ITEM_NORMAL)
                if num != 2:
                    menu.AppendSeparator()
                self.Bind(wx.EVT_MENU, handler, item)
            menubar.Append(menu, title)

        self.SetMenuBar(menubar)

    def _console_log(self):
        self.listInput = wx.TextCtrl(self.panel, -1, '', (240, 50), (525, 400),
                                     style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL,
                                     name="InputText")
        redir = RedirectText(self.listInput)
        sys.stdout = redir

    def file_export(self, event):
        export_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        default_name = '{}执行记录.txt'.format(export_time)
        self.wildcard = '文本文件(*.txt)|*.txt|所有文件(*.*)|*.*'
        dlg = wx.FileDialog(self, '导出', os.getcwd(),
                            defaultFile=default_name,
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                            wildcard=self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            file = open(dlg.GetPath(), 'w')
            file.write(self.listInput.GetValue())
            file.close()
            dlg.Destroy()
        # print(self.listInput.GetValue())

    def pg_exit(self, event):
        dial = wx.MessageDialog(None, "确定退出吗?", "提示",
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()

        if ret == wx.ID_YES:
            self.Destroy()
        else:
            pass
            # event.Veto()

    def _submit_event(self, event):
        self.submit_button = event.GetEventObject()
        if len(self.listBox.GetSelections()) <= 0:
            warning = wx.MessageDialog(None, "还未选定文件，请重新选择", "错误",
                                       wx.OK | wx.ICON_QUESTION)
            warning.ShowModal()
        else:
            dial = wx.MessageDialog(None, "确定运行选中的{}项吗?".format(len(self.listBox.GetSelections())), "提示",
                                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            ret = dial.ShowModal()
            if ret == wx.ID_YES:
                self.select_file = []
                for file_num in self.listBox.GetSelections():
                    self.select_file.append(self.check_list[file_num])
                self.run_path(self.select_dir, self.select_file)
            else:
                pass
                # event.Veto()
        # print(self.select_file)

    def run_path(self, run_dir='WebTest', *run_list):
        os.chdir('./{}'.format(run_dir))
        try:
            for i in run_list[0]:
                i = 'python {}.py'.format(i)
                print("运行{}/{}".format(run_dir, i[7:]))
                p = os.system(i)
                if p == 0:
                    print("{}执行结果:成功".format(i))
                else:
                    print("{}执行结果:失败，详情请见日志".format(i))
            os.chdir('../')
        except IndexError as e:
            os.chdir('../')
            print(e)

    def _menu_about(self, event):
        about = wx.MessageDialog(None, "v0.1  Copyright by adonet", "关于",
                                 wx.OK | wx.ICON_QUESTION)
        about.ShowModal()

    # 第二种事件绑定实现方式
    def menu_handler(self, event):
        id = event.GetId()
        if id == wx.ID_SAVEAS:
            wx.MessageBox(u'导出文件', '导出..', wx.OK | wx.ICON_INFORMATION)
        if id == wx.ID_CLOSE:
            wx.MessageBox(u'退出程序', '提示', wx.OK | wx.ICON_INFORMATION)


class RedirectText:
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.out.WriteText(' | {} | '.format(time_now))
        self.out.WriteText(string)


# TODO:无效类
class ProgramControl:
    def __init__(self):
        pass

    @staticmethod
    def change_dir(dir_num=0):
        os.chdir('./{}'.format(index_list[dir_num]))


def main():
    app = App(redirect=False)
    app.MainLoop()


if __name__ == '__main__':
    index_list = ['AppTest', 'MultiThreading', 'WebTest']
    main()
