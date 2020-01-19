import os
import threading


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


def main(run_dir='WebTest', *run_list):
    os.chdir('./{}'.format(run_dir))
    try:
        for i in run_list[0]:
            i = 'python {}'.format(i)
            print("{}\n运行{}/{}\n{}".format('*' * 30, run_dir, i[7:], '*' * 30))
            p = os.system(i)
            if p == 0:
                print("{}\n{}结果:运行成功\n{}".format('*' * 30, i, '*' * 30))
            else:
                print("{}\n{}结果:运行失败\n{}".format('*' * 30, i, '*' * 30))
    except IndexError as e:
        print(e)
    check_turn = True
    while check_turn:
        run_check = input('是否需要继续执行？(Y/N)')
        if run_check.lower() == 'n':
            print('所有文件已运行完毕')
            check_turn = False
        elif run_check.lower() == 'y':
            print('正在跳转...')
            os.chdir('../')
            choose_list()
            check_turn = False
        else:
            print('您输入的数据有误，请重新输入')


def choose_list():
    global choose_num
    dir_list = {1: 'AppTest', 2: 'MultiThreading', 3: 'WebTest'}
    choose_turn = True
    while choose_turn:
        choose_num = input("请输入执行文件夹序号：{}\n".format(dir_list))
        choose_num = int(choose_num)
        if choose_num == 1 or choose_num == 2 or choose_num == 3:
            os.chdir('./{}'.format(dir_list[choose_num]))
            choose_turn = False
        else:
            print('您输入的序号有误，请重新输入')
    dirs = os.listdir('./')
    file_list = {}
    a = 1
    for i in dirs:  # 循环读取路径下的文件并筛选输出
        if os.path.splitext(i)[1] == ".py":  # 筛选执行文件
            a = a + 1
            file_list[a - 1] = i
            # print(i)
    print(file_list)
    file_choose = input('请输入要执行的文件序号，用空格隔开:\n').split()
    final_list = []
    for i in file_choose:
        try:
            i = int(i)
            final_list.append(file_list[i])
        except KeyError:
            print('输入数字有误，自动跳过')
            pass
    print(final_list)
    # print(os.getcwd())  # 查看当前工作目录
    os.chdir('../')
    main(dir_list[choose_num], final_list)


if __name__ == '__main__':
    choose_list()
