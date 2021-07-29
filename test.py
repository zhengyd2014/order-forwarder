from datetime import datetime, time

timeStr = '2021-07-28T22:20:26.181Z'


now = datetime.now()
n = now.strftime("%Y-%m-%d %H:%M:%S")

print(n)
