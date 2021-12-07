
import schedule
import time
import datetime as dt
import main3

def job():
    print(main3.trade())
# def job2():
#     print(dt.datetime.now())

for t in ['14:55','15:55','16:55','17:55','18:55','19:55']:
    schedule.every().monday.at(t).do(job)
    schedule.every().tuesday.at(t).do(job)
    schedule.every().wednesday.at(t).do(job)
    schedule.every().thursday.at(t).do(job)
    schedule.every().friday.at(t).do(job)
# schedule.every().friday.at('15:53').do(job2)
# schedule.every().friday.at('15:55').do(job2)

# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
while 1:
    schedule.run_pending()
    time.sleep(1)
