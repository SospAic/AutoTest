import wx


class ListBoxFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'List Box Example',
                          size=(1200, 800))
        panel = wx.Panel(self, -1)

        sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
                      'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
                      'twelve', 'thirteen', 'fourteen']

        listBox = wx.ListBox(panel, -1, (20, 20), (200, 520), sampleList, wx.LB_MULTIPLE,
                             validator=wx.DefaultValidator, )
        listBox.SetSelection(0)
        # listBox.Clear()
        print(listBox.FindString('eight'))

        listText = wx.StaticText(panel, -1, '示例文本', (240, 20), (200, 520), style=0, name="staticText")
        listText.AcceptsFocus()
        listText.SetLabelText('Hello World')

        listInput = wx.TextCtrl(panel, -1, '示例文本框', (440, 20), (200, 520), style=0, name="InputText")
        listInput.AcceptsFocusFromKeyboard()
        # listInput.SetLabelText('Hello World')

        IndexFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=False, faceName="",
                            encoding=wx.FONTENCODING_DEFAULT)

        listInput.SetFont(IndexFont)
        listInput.SetBackgroundColour('#0a74f7')

        SimpleButton = wx.Button(panel, -1, '示例按钮', (640, 20), size=wx.DefaultSize, style=0)

        # wx.BitmapButton(panel, -1, 'bmp', (640, 60), size=wx.DefaultSize, style=0)

        SToggleButton = wx.ToggleButton(panel, -1, u"开关", (640, 60), size=wx.DefaultSize, style=0)

        wx.Slider(panel, -1, 100, 0, 800, (840, 20), size=wx.DefaultSize,
                  style=wx.SL_AUTOTICKS, validator=wx.DefaultValidator, name="slider")

        MultiCheckbox = wx.CheckBox(panel, -1, '示例多选框', (1040, 20), size=wx.DefaultSize, style=0, name="checkBox")

        # listMultiText = wx.TE_MULTILINE(panel, -1, '示例多文本', (640, 20), (200, 520), style=0, name="staticText")
        # listText.AcceptsFocus()

        wx.RadioButton(panel, -1, '单选按钮', (1040, 60), size=wx.DefaultSize, style=0,
                       validator=wx.DefaultValidator, name="radioButton")

        wx.RadioBox(panel, -1, '单选框', (640, 100), (240, 160), choices=sampleList, majorDimension=3,
                    style=wx.RA_SPECIFY_COLS, validator=wx.DefaultValidator, name="radioBox")

        wx.Choice(panel, -1, pos=(890, 100), size=(240, 160), choices=sampleList, style=0,
                  validator=wx.DefaultValidator, name="choice")

        wx.ComboBox(panel, -1, value="", pos=(890, 200), size=(240, 160), choices=sampleList, style=0,
                    validator=wx.DefaultValidator, name="comboBox")

        wx.Frame(panel, id=-1, title="Hello World", pos=(140, 20),
                 size=(240, 160), style=wx.FRAME_FLOAT_ON_PARENT,
                 name="frame")


if __name__ == '__main__':
    app = wx.PySimpleApp()
    ListBoxFrame().Show()
    app.MainLoop()
