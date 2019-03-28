# encoding:utf-8
import os


message = "Hello world"
num = 123
array = [78, -1, 88, 532, 0, 7, 9, 22, 34, 56]
dic = {'username', 'password'}
print(message, num, array, dic)
print(message.title(), message.upper(), message.lower())
languages = "\tJava\n\tC\n\tPython\n\tRuby"
print(languages)
check_string = "看看你 能  找到几个空格 "
print(check_string.rstrip())
print(3/2)
array.remove(7)
print(array)
get_code = array.pop(0)
print(get_code, sorted(array), array[-1])
print(array)
array.sort(reverse=True)
print(array)
for i in array:
    print(i)
create_array = list(range(1, 10, 2))
print(sum(create_array))
squals = [value**2 for value in range(1, 50, 3)]
print(squals, squals[0:3], squals[-4:])
squals_1 = squals[:]
print(squals_1)
str_1 = "haha,hehe,123,456,:D"
list_1 = str_1.split(',')
print(list_1)
str_2 = ".".join(list_1)
print(str_2)
list_2 = ('可以修改吗', '可以试试')
print(list_2)
# list_2[0] = '我改'
print(21 >= 20 or 12 == 13)
dictionary = {'路人甲': '张三', '路人乙': '李四', '路人丙': '周五', '路人丁': '郑王', }
print(dictionary['路人甲'].title())
for key, value in dictionary.items():
    print(key, value)
people = ['路人甲', '路人乙']
for key in dictionary.keys():
    if key in people:
        print(key)
    print(key)
person = []
for add_person in range(30):
    add_person = {'姓名': '我是A', '年龄': '25', '星座': '射手'}
    person.append(add_person)
print(person)
text_1 = "hello,"
text_1 += "\nwhat's ur name?\n"
text_2 = input(text_1)
print("hello " + text_2 + "!")
autherised_user = []
while person:
    autherised_user.append(person.pop())
    print(autherised_user)
print(dictionary['路人甲'])

