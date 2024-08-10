import time
from multiprocessing import Process

def worker ():
    while True:
        print("Inside the worker")
        time.sleep(10)

def proc_start():
    p_to_start = Process(target=worker,name="worker")
    p_to_start.start()
    return p_to_start


def proc_stop(p_to_stop):
    p_to_stop.terminate()
    print("after Termination ")


p = proc_start()
time.sleep(3)
proc_stop(p)
time.sleep(3)

p = proc_start()
print("start gain")
time.sleep(3)