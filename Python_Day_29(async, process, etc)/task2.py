from task1 import time_decor, pretty_print_decor, TIME
import random
import time
import threading
import multiprocessing
import asyncio
from functools import wraps

NUMBERS = [10_000_000, 10_000_000, 10_000_000, 10_000_000]

def heavy_calculation(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total

async def async_calc(n):
    return heavy_calculation(n)

@time_decor
@pretty_print_decor('Синхронный подход')
def base_way():
    results = []
    for n in NUMBERS:
        results.append(heavy_calculation(n))
    print('Расчеты закончены')
    return results

@time_decor
@pretty_print_decor('Асинхронный подход')
async def async_main():
    tasks = [async_calc(n) for n in NUMBERS]
    print('Расчеты закончены')
    return await asyncio.gather(*tasks)

@time_decor
@pretty_print_decor('Поточный подход')
def threaded():
    results = [None] * len(NUMBERS)

    def worker(idx, n):
        results[idx] = heavy_calculation(n)

    threads = []

    for i, n in enumerate(NUMBERS):
        t = threading.Thread(target=worker, args=(i, n))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print('Расчеты закончены')
    return results

@time_decor
@pretty_print_decor('Мультипроцессорный подход')
def multiprocess():
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(heavy_calculation, NUMBERS)
    print('Расчеты закончены')
    return results

if __name__ == '__main__':
    print('--------------------------------------')
    base_way()
    print('--------------------------------------')
    asyncio.run(async_main())
    print('--------------------------------------')
    threaded()
    print('--------------------------------------')
    multiprocess()
    print('')
    print('')
    score = [print(f'Функция - {name_f}, время - {time}') for name_f, time in TIME.items()]

