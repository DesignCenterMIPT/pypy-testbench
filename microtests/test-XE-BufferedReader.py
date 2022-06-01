import sys
import io


with open('data/test.bin', 'rb') as file:
    # file descriptor is obtained by making using of FileIO which is used to identify the file that is opened
    fi_io  = io.FileIO(file.fileno())
    # Buffered reader is then used to read the contents of the file
    br_io = io.BufferedReader(fi_io)
    
    for _ in range(100000):
       reading = br_io.read()

