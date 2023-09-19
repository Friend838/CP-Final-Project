# from StopableSleepingThread import StopableThread
import threading
import time

def sleep(event, seconds):
    event.wait(seconds)
    
    if event.is_set():
        print("T1 stop waiting")
    else:
        print("T1 wait till finish")

if __name__ == "__main__":
    e1 = threading.Event()
    e2 = threading.Event()
    
    t1 = threading.Thread(target=sleep, args=(e1, 100))
    t2 = threading.Thread(target=sleep, args=(e2, 100))
    
    t1.start()
    t2.start()
    
    print(t1.is_alive())
    print(t2.is_alive())
    
    for i in range(10):
        print(i)
        time.sleep(1)
    e1.set()
    time.sleep(0.1)
    print(t1.is_alive())
    print(t2.is_alive())
    
    for i in range(10, 20):
        print(i)
        time.sleep(1)
    e2.set()
    time.sleep(0.1)
    print(t1.is_alive())
    print(t2.is_alive())