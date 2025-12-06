import random
import time
import threading
import multiprocessing
import asyncio
from functools import wraps

TIME = {}

def time_decor(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        t_start = time.perf_counter()
        await func(*args, **kwargs)
        all_time = time.perf_counter() - t_start
        print('Время выполнения:',"{:.2f}".format(all_time), 'сек.')
        TIME[f"{func.__name__}"] = '{:.2f}'.format(all_time)

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        t_start = time.perf_counter()
        func(*args, **kwargs)
        all_time = time.perf_counter() - t_start
        print('Время выполнения:',"{:.2f}".format(all_time), 'сек.')
        TIME[f"{func.__name__}"] = '{:.2f}'.format(all_time)

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper

def pretty_print_decor(text:str):
    def decor(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            print(f'{text}')
            print('======================================')
            await func(*args, **kwargs)
            print('======================================')
            print(f'Завершаем {text}')

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            print(f'{text}')
            print('======================================')
            func(*args, **kwargs)
            print('======================================')
            print(f'Завершаем {text}')

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decor

def network_request(id: str) -> None:
    """Функция, которая имитирует сетевые запросы"""
    if type(id) != str:
        id = str(id)
    print(f'Начинаю обработку ID:{id}')
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
    print(f"ID:{id} - успешно обработана за {delay:.2f}")

async def async_network_request(id: str) -> None:
    """Функция, которая имитирует сетевые запросы(асинхронная)"""
    if type(id) != str:
        id = str(id)
    print(f'Начинаю обработку ID:{id}')
    delay = random.uniform(0.5, 2.0)
    await asyncio.sleep(delay)
    print(f"ID:{id} - успешно обработана за {delay:.2f}")

@time_decor
@pretty_print_decor(text="Синхронный подход")
def base_way(ids: list) -> None:
    result = [network_request(id) for id in ids]

@time_decor
@pretty_print_decor(text="Асинхронный подход")
async def async_way(ids:list) -> None:
    tasks = [async_network_request(id) for id in ids]
    await asyncio.gather(*tasks)

@time_decor
@pretty_print_decor(text="Потоковый подход")
def thread_way(ids:list) -> None:
    threads = []
    for id in ids:
        t = threading.Thread(target=network_request, args=(id,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

@time_decor
@pretty_print_decor(text="Мультипроцессорный подход")
def m_process_way(ids:list) -> None:
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(network_request, ids)

if __name__ == "__main__":
    ids = [str(random.randint(1, 1000)) for _ in range(20)] #переменная, которая генерирует 20 id, с числом в промежутке от 1 до 999

    print('Операции ограниченные I/O')
    print('------------------------------------------')
    base_way(ids)
    print('------------------------------------------')
    m_process_way(ids)
    print('------------------------------------------')
    thread_way(ids)
    print('------------------------------------------')
    asyncio.run(async_way(ids))
    print('------------------------------------------')
    score = [print(f'Функция - {name_f}, время - {time}') for name_f, time in TIME.items()]

