import os
import wx
import TestIndex


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
        self.Bind(wx.EVT_LISTBOX, self._get_elements, self.listBox)

    def create_widgets(self):
        self._create_menubar()
        self.CreateStatusBar()
        self.control_window()

    def control_window(self):
        panel = wx.Panel(self, -1)
        wx.Choice(panel, -1, pos=(10, 10), size=(200, 160), choices=index_list, style=0,
                  validator=wx.DefaultValidator, name="choice")
        self.listBox = wx.ListBox(panel, -1, (10, 40), (200, 400), index_list, wx.LB_MULTIPLE,
                                  validator=wx.DefaultValidator, )
        self.listBox.SetSelection(0)
        print(self.listBox.FindString('MultiThreading'))

        self.listText = wx.StaticText(panel, -1, '示例文本', (230, 15), (200, 15), style=0, name="staticText")
        self.listText.SetLabelText('Hello World')
        indexFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=False, faceName="",
                            encoding=wx.FONTENCODING_DEFAULT)
        self.submit_button = wx.Button(panel, -1, u"确定", (10, 460), size=wx.DefaultSize, style=0)
        self.cancel_button = wx.Button(panel, -1, u"取消", (120, 460), size=wx.DefaultSize, style=0)
        self.MultiCheckbox = wx.CheckBox(panel, -1, '示例多选框', (230, 45), size=wx.DefaultSize, style=0, name="checkBox")

    def _get_elements(self, event):
        self.listBox = event.GetEventObject()
        print("选择{0}".format(self.listBox.GetSelections()))

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

    def file_new(self, event):
        print('file_new')

    def file_open(self, event):
        print('file_open')

    def file_save(self, event):
        print('file_save')

    def file_saveas(self, event):
        print('file_saveas')


class ProgramControl:
    def __init__(self):
        pass

    @staticmethod
    def change_dir(dir_num=0):
        os.chdir('./{}'.format(index_list[dir_num]))


def main():
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    index_list = ['AppTest', 'MultiThreading', 'WebTest']
    main()
