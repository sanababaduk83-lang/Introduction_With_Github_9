class Iterablelol:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return (i for i in range(self.n))


obj = Iterablelol(5)

for x in obj:
    print(x)
