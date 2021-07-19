import re

str1 = '|  黑龙江联通  |  第2级  |  已提交  |  2020/02/12  |  省网络管理中心  |  '
print(str1)
if '|' in str1:
    print('ok')
temp = re.split('[ ,|;*]+', str1)
print(temp)
for i in temp:
    print(i)
    if i == '':
        temp.remove(i)
print(str(temp))