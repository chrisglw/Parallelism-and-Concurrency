from datetime import datetime, timedelta
import time
import threading
import random

# Include cse251 common Python files
from cse251 import *
import multiprocessing

# Global Consts
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

# Same Car and Queue251 classes

class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """
    def __init__(self, semaphore, lock, queue, barrier):
        threading.Thread.__init__(self)
        self.semaphore = semaphore
        self.lock = lock
        self.queue = queue
        self.barrier = barrier
        self.cars_to_produce = random.randint(200, 300)     # Don't change

    def run(self):
        for _ in range(self.cars_to_produce):
            car = Car()
            self.semaphore.acquire()
            with self.lock:
                self.queue.put(car)
            self.semaphore.release()

        self.barrier.wait()

class Dealer(threading.Thread):
    """ This is a dealer that receives cars """
    def __init__(self, semaphore, lock, queue, barrier, dealer_stats, dealer_id):
        threading.Thread.__init__(self)
        self.semaphore = semaphore
        self.lock = lock
        self.queue = queue
        self.barrier = barrier
        self.dealer_stats = dealer_stats
        self.dealer_id = dealer_id

    def run(self):
        while True:
            self.semaphore.acquire()
            with self.lock:
                if self.queue.items:
                    self.queue.get()
                    self.dealer_stats[self.dealer_id] += 1
            self.semaphore.release()

            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))

            if self.barrier.broken:
                break

def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """
    log = Log(show_terminal=True)
    
    # Semaphore and Lock
    semaphore = threading.Semaphore(MAX_QUEUE_SIZE)
    lock = threading.Lock()
    
    # Queue
    car_queue = Queue251()

    # Barrier
    barrier = threading.Barrier(factory_count + dealer_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)

    # Factories
    factories = [Factory(semaphore, lock, car_queue, barrier) for _ in range(factory_count)]

    # Dealerships
    dealerships = [Dealer(semaphore, lock, car_queue, barrier, dealer_stats, i) for i in range(dealer_count)]

    log.start_timer()

    # Start all dealerships and factories
    for dealer in dealerships:
        dealer.start()
    for factory in factories:
        factory.start()

    # Wait for factories and dealerships to complete
    for factory in factories:
        factory.join()
    for dealer in dealerships:
        dealer.join()

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    factory_stats = [factory.cars_to_produce for factory in factories]

    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)

# main function remains the same
