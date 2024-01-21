import time
import logging


def retry_on_exception(exception_list: list, max_attempts: int):
    """Декоратор ловит ошибки во время выполнения ф-ции, так же считает кол-во попыток"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            count_attempts = 0
            while count_attempts < max_attempts:
                try:
                    res = func(*args, **kwargs)
                    return res
                except tuple(exception_list) as e:
                    count_attempts += 1
                    logging.warning(f'Попытка {count_attempts} провалилась с исключением {e}')
                    time.sleep(1)
            else:
                logging.error(f'Достигнуто максимльное кол-во попыток {count_attempts}/{max_attempts}')

        return wrapper

    return decorator


@retry_on_exception([ZeroDivisionError, KeyError], max_attempts=3)
def divide_numbers(x, y):
    """Ф-ция делить 2 числа"""
    return x / y


print(divide_numbers(10, 0))
