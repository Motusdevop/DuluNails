import datetime

current_datetime = datetime.datetime.now()
print(current_datetime)

date = datetime.datetime(year=current_datetime.year, month=2, day=7, hour=16, minute=30)

formatted_datetime = date.strftime("%m.%d c %H:%M")
print(formatted_datetime)

print(date)

