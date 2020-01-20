import logging
import os
import sys
import wx.lib.newevent
import wx
import TestIndex


# wxLogEvent, EVT_WX_LOG_EVENT = wx.lib.newevent.NewEvent()
#
#
# class wxLogHandler(logging.Handler):
#     """
#     A handler class which sends log strings to a wx object
#     """
#
#     def __init__(self, wxdest=None):
#         """
#         Initialize the handler
#         @param wxdest: the destination object to post the event to
#         @type wxdest: wx.Window
#         """
#         logging.Handler.__init__(self)
#         self.wxDest = wxdest
#         self.level = logging.DEBUG
#
#     def flush(self):
#         """
#         does nothing for this handler
#         """
#
#     def emit(self, record):
#         """
#         Emit a record.
# """
#         try:
#             msg = self.format(record)
#             evt = wxLogEvent(message=msg, levelname=record.levelname)
#             wx.PostEvent(self.wxDest, evt)
#         except (KeyboardInterrupt, SystemExit):
#             raise
#         except:
#             self.handleError(record)


class App(wx.App):
    def OnInit(self):
        main_window = MainWindow(None, title='批处理图形化界面')
        main_window.Show()
        # self.SetTopWindow(main_window)
        return True


class MainWindow(wx.Frame):
    def __init__(self, *args, size=(800, 600), **kwargs):
        super().__init__(*args, size=size, **kwargs)
        self.create_widgets()
        self.Bind(wx.EVT_LISTBOX, self._get_dir_elements, self.listBox)
        self.Bind(wx.EVT_CHOICE, self._get_dir, self.menu_select)
        # self.Bind(EVT_WX_LOG_EVENT, self.console_log)

    def create_widgets(self):
        self._create_menubar()
        self.CreateStatusBar()
        self.control_window()
        self._console_log()

    def control_window(self):
        self.panel = wx.Panel(self, -1)
        self.menu_select = wx.Choice(self.panel, -1, pos=(20, 15), size=(200, 160), choices=index_list, style=0,
                                     validator=wx.DefaultValidator, name="choice")
        self.check_list = ['1', '2', '3']
        self.listBox = wx.ListBox(self.panel, -1, (20, 50), (200, 400), self.check_list, wx.LB_MULTIPLE,
                                  validator=wx.DefaultValidator, )
        self.listText = wx.StaticText(self.panel, -1, '示例文本', (230, 15), (200, 15), style=0, name="staticText")
        self.listText.SetLabelText('Hello World')
        indexFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=False, faceName="",
                            encoding=wx.FONTENCODING_DEFAULT)
        self.submit_button = wx.Button(self.panel, -1, u"确定", (20, 460), size=wx.DefaultSize, style=0)
        self.cancel_button = wx.Button(self.panel, -1, u"取消", (130, 460), size=wx.DefaultSize, style=0)
        self.MultiCheckbox = wx.CheckBox(self.panel, -1, '示例多选框', (230, 45), size=wx.DefaultSize, style=0,
                                         name="checkBox")

    def _get_dir_elements(self, event):
        self.listBox = event.GetEventObject()
        print("选择{0}".format(self.listBox.GetSelections()))

    def _get_dir(self, event):
        self.menu_select = event.GetEventObject()
        select_num = self.menu_select.GetSelection()
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
            print(self.check_list)
            self.listBox.Set(self.check_list)
            os.chdir('../')
            print("选择{0}".format(self.menu_select.GetSelection()))
        else:
            print('索引值错误')
            pass

    def _create_menubar(self):
        menubar = wx.MenuBar()
        menus = {
            'File': (
                (wx.ID_NEW, 'New\tCtrl+N', 'New file', self.file_new),
                (wx.ID_OPEN, 'Open\tCtrl+O', 'Open file', self.file_open),
                (wx.ID_SAVE, 'Save\tCtrl+S', 'Save file', self.file_save),
                (wx.ID_SAVEAS, 'Save as\tCtrl+Shift+S', 'Save as', self.file_saveas)
            )
        }

        for title, items in menus.items():
            menu = wx.Menu()
            for id_, label, help_string, handler in items:
                item = menu.Append(id_, label, help_string)
                self.Bind(wx.EVT_MENU, handler, item)
            menubar.Append(menu, title)

        self.SetMenuBar(menubar)

    def _console_log(self):
        # msg = event.message.strip("\r") + "\n"
        # self.listInput.AppendText(msg)  # or whatevery
        # event.Skip()
        self.listInput = wx.TextCtrl(self.panel, -1, '', (240, 230), (525, 220),
                                     style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL,
                                     name="InputText")
        wx.CallAfter(self.dologging)
        self.log_window = wx.LogTextCtrl(self.listInput)
        wx.Log.SetActiveTarget(self.log_window)

    def write(self, s):
        self.listInput.AppendText(s)

    def dologging(self):
        print('do logging...')
        # ~ logging.warning('This message should go to my wxTextCtrl...')
        wx.LogMessage('sys.stderr')
        wx.CallLater(3000, self.dologging)

    def file_new(self, event):
        print('file_new')

    def file_open(self, event):
        print('file_open')

    def file_save(self, event):
        print('file_save')

    def file_saveas(self, event):
        print('file_saveas')


# TODO:无效类
class ProgramControl:
    def __init__(self):
        pass

    @staticmethod
    def change_dir(dir_num=0):
        os.chdir('./{}'.format(index_list[dir_num]))


def main():
    # app = App(redirect=True, filename=r'./GUI输出日志.txt')
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    index_list = ['AppTest', 'MultiThreading', 'WebTest']
    main()
