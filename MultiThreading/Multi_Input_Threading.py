# -*- coding:UTF-8 -*-

import threading
import queue


# 重写进程，获取返回值
class MyThread(threading.Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


# 线程创建（阻塞）
class InputThreading:
    def __init__(self, input_text, output_text, time_out):
        self.e = threading.Event()
        self.input_thread = MyThread(self.get_input, args=(input_text, output_text))
        self.wait_thread = MyThread(self.wait_event, args=(time_out,))
        self.input_thread.daemon = True
        self.wait_thread.start()
        self.input_thread.start()
        self.wait_thread.join(time_out)  # 加入阻塞及超时时间
        self.input_thread.join(time_out)  # 加入阻塞及超时时间

    def get_input(self, in_text=None, out_text=None):
        num = input(in_text)
        print('')
        self.e.set()
        print(num)
        return num

    def wait_event(self, time_out=None):
        self.e.wait(timeout=time_out)


# 线程创建+加入队列（阻塞）
class InputThreadingQueue:
    def __init__(self, t_input, t_output, tim_out):
        self.que = queue.Queue()
        self.input_thread = MyThread(self.get_input, args=(t_input, t_output))
        self.wait_thread = MyThread(self.wait, args=(tim_out,))
        self.input_thread.daemon = True
        self.wait_thread.start()
        self.input_thread.start()
        self.wait_thread.join(tim_out)  # 加入阻塞及超时时间
        self.input_thread.join(tim_out)  # 加入阻塞及超时时间

    def get_input(self, text_input, text_output):
        print(text_output, input(text_input))
        self.que.put(1)

    def wait(self, time_out):
        try:
            self.que.get(timeout=time_out)
        except queue.Empty:
            pass


if __name__ == '__main__':
    # q = queue.Queue()
    # input_threading()
    a = InputThreadingQueue('请输入：', '结果为：', 5)
    print(a.input_thread.get_result())
    b = InputThreading('请输入：', '结果为：', 5)
    print(b.input_thread.get_result())
