import my_module as m

def congruent(a : int, b: int, p: int) -> bool:
    return a % p == b

def divisor(a: int, b: int) -> bool:
    return b % a == 0

def prime(a) -> bool:
    if a < 2:
        return False
    for i in range(2, int(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True


def test_congruence():
    a = m.congruent(5,2,3)
    b = not m.congruent(1,4,2)
    return a and b

def test_divisor():
    a = m.divisor(2,12)
    b = not m.divisor(5,7)
    return a and b

def test_prime():
    a = m.prime(37)
    b = not m.prime(8)
    return a and b

if __name__ == "__main__":
    test = {
        'test_congruence' : test_congruence(),
        'test_divisor' : test_divisor(),
        'test_prime' : test_prime()
    }

    for name, result in test.items():
        if result:
            print(f'{name} : PASSED')
        else:
            print(f'{name} : FAILED')