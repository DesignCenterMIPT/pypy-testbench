from sympy.utilities.iterables import ordered


seq, keys = [[[1, 2, 1], [0, 3, 1], [1, 1, 3], [2], [1]], 
        [lambda x: len(x), lambda x: sum(x)]]

check_lst = list(ordered(seq, keys, default=False, warn=False))

