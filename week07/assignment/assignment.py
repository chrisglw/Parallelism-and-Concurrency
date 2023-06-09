
from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = mp.Manager().list()
result_words = mp.Manager().list()
result_upper = mp.Manager().list()
result_sums = mp.Manager().list()
result_names = mp.Manager().list()

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
 
def task_prime(value: int) -> str:
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    return f"{value} is prime" if is_prime(value) else f"{value} is not prime"
    # pass

def task_word(word: str) -> str:
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt', 'r') as f:
        words = f.read().splitlines()
    return f"{word} Found" if word in words else f"{word} not found"
    # pass

def task_upper(text: str) -> str:
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    return f"{text} ==> {text.upper()}"
    # pass

def task_sum(start_value: int, end_value: int) -> str:
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = sum(range(start_value, end_value + 1))
    return f"sum of {start_value:,} to {end_value:,} = {total:,}"
    # pass

def task_name(url: str) -> str:
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        name = response.json().get('name')
        if name is not None:
            return f"{url} has name {name}"
    return f"{url} had an error receiving the information"
    # pass


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pool_prime = mp.Pool(5)
    pool_word = mp.Pool(5)
    pool_upper = mp.Pool(5)
    pool_sum = mp.Pool(5)
    pool_name = mp.Pool(5)

    # TODO you can change the following
    # TODO start and wait pools
    
    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            pool_prime.apply_async(task_prime, args=(task['value'], ), callback=lambda x: result_primes.append(x))
        elif task_type == TYPE_WORD:
            pool_word.apply_async(task_word, args=(task['word'], ), callback=lambda x: result_words.append(x))
        elif task_type == TYPE_UPPER:
            pool_upper.apply_async(task_upper, args=(task['text'], ), callback=lambda x: result_upper.append(x))
        elif task_type == TYPE_SUM:
            pool_sum.apply_async(task_sum, args=(task['start'], task['end']), callback=lambda x: result_sums.append(x))
        elif task_type == TYPE_NAME:
            pool_name.apply_async(task_name, args=(task['url'], ), callback=lambda x: result_names.append(x))
        else:
            log.write(f'Error: unknown task type {task_type}')

    pool_prime.close()
    pool_prime.join()

    pool_word.close()
    pool_word.join()

    pool_upper.close()
    pool_upper.join()

    pool_sum.close()
    pool_sum.join()

    pool_name.close()
    pool_name.join()


    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
