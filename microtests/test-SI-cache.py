from functools import lru_cache, wraps
from random import choice


def test_cache(func):
    cfunc = lru_cache(maxsize=20, typed=True)(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            retval = cfunc(*args, **kwargs)
        except TypeError:
            retval = func(*args, **kwargs)

        return retval
    return wrapper


@test_cache
def test_func(st: set):
    total_mul: int = 1
    for elem in st:
        total_mul *= elem
    
    return total_mul


if __name__ == "__main__":
    choices = [i for i in range(20)]

    for i in range(100000):
        st = set([choice(choices) for j in range(10)])
        test_func(st)
    
