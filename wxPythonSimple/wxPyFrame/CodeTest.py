import wx
from wx import FontEnumerator

aaa = wx.App(False)
e = wx.FontEnumerator()
fontList = e.GetFacenames()
for i in fontList:
    print(i)
