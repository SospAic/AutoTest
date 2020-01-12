import threading


#
#
# def get_input(in_text, out_text, e):
#     print(out_text, input(in_text))
#     e.set()
#
#
# def wait_event(time_out, e):
#     e.wait(timeout=time_out)
import time


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


class InputThreading:
    def __init__(self, input_text, output_text, time_out):
        self.e = threading.Event()
        self.input_thread = MyThread(self.get_input, args=(input_text, output_text))
        self.wait_thread = MyThread(self.wait_event, args=(time_out,))
        self.input_thread.daemon = True
        self.wait_thread.start()
        self.input_thread.start()

    def get_input(self, in_text=None, out_text=None):
        num = input(in_text)
        print('')
        self.e.set()
        return num

    def wait_event(self, time_out=None):
        self.e.wait(timeout=time_out)
        return self.input_thread.get_result()


if __name__ == '__main__':
    # e = threading.Event()
    # input_thread = threading.Thread(target=get_input, args=('in_text', 'out_text', e))
    # wait_thread = threading.Thread(target=wait_event, args=(2, e))
    # input_thread.daemon = True
    # wait_thread.start()
    # input_thread.start()
    a = InputThreading('123', '456', 3)
    # print(a.input_thread.get_result())
