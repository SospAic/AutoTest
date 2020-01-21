"""
@Author : 行初心
@Date   : 18-9-23
@Blog   : www.cnblogs.com/xingchuxin
@Gitee  : gitee.com/zhichengjiu
"""


def main():
    # 看下面的列子,长度11,最后一个索引10
    new_members = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    print(new_members)

    arg = 1
    ind = new_members.index(arg)
    print('整个列表的第一个索引:' + str(ind))

    arg = 1
    # 从索引值为3 开始搜索  到  索引值为11-1
    ind = new_members.index(arg, 3, 11)
    print('列表中指定索引范围的第一个索引:' + str(ind))


if __name__ == '__main__':
    main()
