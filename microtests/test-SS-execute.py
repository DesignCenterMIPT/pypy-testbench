import sqlite3
import math


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    cos_i = math.cos(1)

    conn.execute('create table cos (x, y, z);')
    for i in range(100000):
        conn.execute('insert into cos values (?, ?, ?)',
                    [i, cos_i, str(i)])

