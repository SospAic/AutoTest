import schedule
import time


def job(name):
    print("her name is : ", name)


def main(method):
    schedule.every(10).minutes.do(job, method)  # 每隔十分钟执行一次任务
    schedule.every().hour.do(job, method)  # 每隔一小时执行一次任务
    schedule.every().day.at("10:30").do(job, method)  # 每天的10:30执行一次任务
    schedule.every(5).to(10).days.do(job, method)  # 每隔5到10天执行一次任务
    schedule.every().monday.do(job, method)  # 每周一的这个时候执行一次任务
    schedule.every().wednesday.at("13:15").do(job, method)  # 每周三13:15执行一次任务
    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)


if __name__ == '__main__':
    main(':D')
