import math
import time


def printO(min, max):
    print("Funktion: ")
    k = 1
    for n in range(min, max):
        print(n)
        # res = (7*k/3)*(n**(math.sqrt(math.pi)))  # first test
        #res = n*n*math.log(10*n)-32*k*(1/(math.e**(n))+math.sqrt(42*n))
        #res = (math.e**(math.sqrt((k)/(math.factorial(n)))))
        timestart = time.time()
        res = 0.35**(n+n**2)
        print(f"{res} time: {time.time()-timestart}", end="")
        timestart = time.time()
        order = 0.35**(n)
        print(f"{res}, time {time.time()-timestart}")


printO(1000000000, 1000000010)
