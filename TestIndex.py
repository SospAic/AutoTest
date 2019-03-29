import os


def main(*run_list):
    try:
        for i in run_list:
            i = 'python %s' % i
            print("运行" + i[7:] + "\n")
            p = os.system(i)
            if p == 0:
                print("\n" + i + "结果:运行成功\n")
            else:
                print("\n" + i + "结果:运行失败\n")
    except IndexError as e:
        print(e)


if __name__ == '__main__':
    main('MySQL.py', 'Get_Code.py', 'Get_Cookie.py')
