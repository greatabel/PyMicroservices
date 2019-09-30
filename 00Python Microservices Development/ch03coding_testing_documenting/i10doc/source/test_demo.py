def suma(x, y):
    z = x + y
    return z


def mulb(x, y):
    z = x * y
    return z


def test_suma():
    assert suma(2, 3) == 5
    assert mulb(2, 3) == 6
