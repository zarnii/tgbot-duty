import pandas as pd
import datetime

ts = pd.date_range('1/1/2020', periods = 366)
ts = pd.Series(ts).apply(str)
new = ts.str.split(" ", n = 1, expand = True)
ts = new[0]

month = ts.apply(lambda x: int(x[5:7]))
mday = ts.apply(lambda x: int(x[8:10]))


def week_day(date):

    year, month, day = (int(x) for x in date.split('-'))
    answer = datetime.date(year, month, day).weekday()
    answer = int(answer) + 1
    return answer
print(ts)

