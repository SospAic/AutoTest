# -*- coding:UTF-8 -*-
import win32api
import win32con
import win32gui


def upload_win_confirm():
    a = win32gui.FindWindow("#32770", "打开")
    print("主窗口", a)
    b = win32gui.FindWindowEx(a, 0, "ComboBoxEx32", None)
    print("二级", b)
    c = win32gui.FindWindowEx(b, 0, "ComboBox", None)
    d = win32gui.FindWindowEx(c, 0, "Edit", None)
    win32gui.SendMessage(d, win32con.WM_SETTEXT, None, r"C:\Users\adonet\Desktop\测试数据\1.jpg")
    # 窗口回车
    win32gui.PostMessage(a, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    # 发送回车
    # win32api.keybd_event(13, 0, 0, 0)
    # win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    # 点击按钮
    # win32gui.SendMessage(b, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    # win32gui.PostMessage(396494, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    # 关闭窗口
    # win32gui.PostMessage(a, win32con.WM_CLOSE, 0, 0)


if __name__ == '__main__':
    upload_win_confirm()
