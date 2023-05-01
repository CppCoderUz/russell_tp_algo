

class Price:
    def __init__(self, i: int, j: int, arg: float) -> None:
        self.i = i
        self.j = j
        self.arg = arg
    def __str__(self) -> str:
        return '%s (%s:%s)'%(
            self.arg,
            self.i,
            self.j,
        )

class Point(object):
    def __init__(self, money: Price, massa: int) -> None:
        self.i = money.i
        self.j = money.j
        self.arg = massa
    
    def __str__(self) -> str:
        return '(%s, %s) %s' %(str(self.i), str(self.j), str(self.arg))



def real_or_int(number: float) -> float|int:
    real_number = float(number)
    int_number = int(number)
    if float(int_number) == real_number:
        return int_number
    else:
        return real_number