for idx in range(4):
    # (-1, 0), (1, 0), (0, -1), (0, 1)
    i = idx % 2 * (idx - 2)
    j = (idx + 1) % 2 * (idx - 1)
    
    print(f'Posición (i, j): ({i}, {j})')

class Test:
    def __init__(self):
        self.a = 1
        self.b = 2

    def __str__(self):
        return f'a: {self.a}, b: {self.b}'

    def __repr__(self):
        return f'a: {self.a}, b: {self.b}'
    
a = Test()

a.x = 2
print(a)

while True:
    choice = int(input("Enter your choice: "))
    print(choice)

