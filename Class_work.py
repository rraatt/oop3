import os
import random
import threading
import timeit

fill = open("Test.txt", "a")


def filler(fill_inp):
    while os.path.getsize("Test.txt") < 52428800:
        fill_inp.write(str(random.randint(0, 9))+'\n')


t = threading.Thread(target=filler, args=[fill])
t2 = threading.Thread(target=filler, args=[fill])
t3 = threading.Thread(target=filler, args=[fill])
t.start()
t2.start()
t3.start()
t.join()
t2.join()
t3.join()

test = """
with open("Test.txt", "r") as read:
    s = 0
    for line in read.readlines():
        if line.strip().isdigit():
            s += int(line.strip())"""


test2 = """
with open("Test.txt", "r") as read:
    s = 0
    for lines in read:
        if lines.strip().isdigit():
            s+= int(lines.strip())"""


test3 = """
with open ("Test.txt", "r") as read:
    k = (int(lines.strip()) for lines in read if lines.strip().isdigit())
    s = sum(k)"""

t = threading.Thread(print("1: " + str(timeit.timeit(test, number=10))))
t2 = threading.Thread(print("2: " + str(timeit.timeit(test2, number=10))))
t3 = threading.Thread(print("3: " + str(timeit.timeit(test3, number=10))))
t.start()
t2.start()
t3.start()
t.join()
t2.join()
t3.join()
# Anyway to make it work concurrently not in order?
