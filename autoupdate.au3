;ControlFocus()��������ʶ��Window����
ControlFocus("��", "","Edit1")

; WinWait()����1�������ڵȴ����ڵ���ʾ
  WinWait("[CLASS:#32770]","",1)

; ControlSetText()�������ļ���������������뱾���ļ���·������������������������ֱ��д�ļ���
  ControlSetText("��", "", "Edit1", "C:\Users\Administrator\Desktop\1.jpg")
  Sleep(1000)

; ControlClick()���ڵ���ϴ������еġ��򿪡���ť

  ControlClick("��", "","Button1");