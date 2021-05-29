import datetime

current_date_time = datetime.datetime.now()
current_time = current_date_time.time()
#print(current_time)

timer = datetime.datetime.strptime('17:51:00.000000', '%H:%M:%S.%f')
print(timer.time())