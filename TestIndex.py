import os


def main():
    run = 'python '
    cust_create = run + 'Custumer_Create.py'  # 集团客户
    reptile = run + 'Get_to_Excel.py'  # 爬虫
    excel_para = run + 'Excel_parameter.py'  # Excel参数化
    run_list = [cust_create, reptile, excel_para]
    print(run_list)
    try:
        for i in run_list:
            print("运行" + i + "\n")
            p = os.system(i)
            if p == 0:
                print("\n" + i + "结果:运行成功\n")
            else:
                print("\n" + i + "结果:运行失败\n")
    except IndexError as e:
        print(e)


if __name__ == '__main__':
    main()
