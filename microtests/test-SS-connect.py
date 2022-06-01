import sqlite3


if __name__ == "__main__":
    for i in range(100000):
        conn = sqlite3.connect(":memory:")
    

