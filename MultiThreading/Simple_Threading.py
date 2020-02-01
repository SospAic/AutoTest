# -*- coding:UTF-8 -*-
import threading

from threading import Timer


class LoopTimer(Timer):
    def __init__(self, interval, function, args=[], kwargs={}):
        Timer.__init__(self, interval, function, args, kwargs)

    def run(self):
        '''self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()'''
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                self.finished.set()
                break
            self.function(*self.args, **self.kwargs)


def fun_timer():
    print('hello timer')  # 打印输出
    global timer  # 定义变量
    timer = threading.Timer(3, fun_timer)  # 60秒调用一次函数
    # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    timer.start()  # 启用定时器
    print('当前线程数为{}'.format(threading.activeCount()))


def func1():
    print('当前线程数为{}'.format(threading.activeCount()))


if __name__ == '__main__':
    t = LoopTimer(2, func1)
    t.start()
