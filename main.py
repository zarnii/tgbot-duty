from datetime import datetime, timedelta
from json_queue import JsonInterface

q = JsonInterface()


def make_duty(names: list, period: int) -> None:
    k = 1
    holidays = q.get_holidays()
    for name in names:
        dates = []
        for j in range(period):
            date = (datetime.now() + timedelta(days=k)).strftime("%d.%m")
            if date not in holidays:
                date_add = (datetime.now() + timedelta(days=k)).strftime("%d.%m.%Y")
                k += 1
                dates.append(date_add)
            else:
                k += 1
            q.enqueue(name, dates)



if __name__ == "__main__":
    make_duty(["zarnii", "zarnii2", "zarnii3"], 10)