from math import sqrt
from dataclasses import dataclass

@dataclass
class Clients:
    x: int
    y: int
    loyal: int

    def check_new(self, x, y):
        distance = sqrt((x-self.x)**2+(y-self.y)**2)
        return distance, self.loyal


clients = []
with open('clients.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        data = line.strip()
        data = data.split(' ')
        client = Clients(int(data[0]), int(data[1]), int(data[2]) )
        clients.append(client)
    #print(clients)


def create_new(x,y):
    closest = {}
    for i in clients:
        closest[i.check_new(x,y)[0]] = i.check_new(x,y)[1]
    sort_keys = sorted(closest.keys())
    a = closest[sort_keys[0]]
    b = closest[sort_keys[1]]
    c = closest[sort_keys[2]]
    if (a + b +c) >= 2:
        print('Да')
    else:
        print('Нет')

x = int(input('Введите х: '))
y = int(input('Введите y: '))

create_new(x,y)