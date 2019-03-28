# encoding:utf-8


class Car(object):
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        long_name = str(self.year) + " " + self.make + " " + self.model
        return long_name.title()

    def update_odometer(self, millage):
        self.odometer_reading += millage
        print(("this car has " + str(self.odometer_reading) + " miles on it.").title())


class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery = Battery()


class Battery:
    def __init__(self, battery_size=70):
        self.battery_size = battery_size

    def describe_battery(self):
        print(("this car has " + str(self.battery_size) + "-KWh in it.").title())


class ReadText:
    def __init__(self, filename='Readme.txt'):
        self.filename = filename

    def read_txt(self):
        with open(self.filename, 'r+') as file_list:
            for line in file_list:
                print(line.rstrip())
            file_list.write('\n添加试试')
        message = "我是谁"
        print(message)
        message.replace("谁", "张三")
        print(message)


class InputNumber:
    def __init__(self, input_n='please check your type'):
        self.input_check = input_n.split()
        print(self.input_check)

    def insert_num(self):
        print("请输入查询选项，q为退出：\n")
        while True:
            self.input_check = input("请输入：\n")
            if self.input_check == 'q' | self.input_check == 'Q':
                break


def count_words(filename):
    try:
        with open(filename, encoding='utf-8') as f_obj:
            contents = f_obj.read()
    except FileNotFoundError:
        pass
    else:
        words = contents.split()
        num_words = len(words)
        print("The file " + filename + " has about " + str(num_words) + " words.")


if __name__ == '__main__':
    my_car = Car('audi', 'a4', 2015)
    print(my_car.get_descriptive_name())
    # my_car.get_descriptive_name = 1
    # print(my_car.get_descriptive_name)
    my_car.update_odometer(23)
    my_car.update_odometer(47)
    my_car.update_odometer(122)
    tesla = ElectricCar('tesla', 'model s', 2017)
    print(tesla.get_descriptive_name())
    tesla.battery.describe_battery()
    txt = ReadText()
    txt.read_txt()
    input_a = InputNumber('hello world')
