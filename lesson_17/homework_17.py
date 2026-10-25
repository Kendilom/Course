import logging
from functools import wraps


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='text.log',
    filemode='w'
)
logger = logging.getLogger('admin')

def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        iteration = 0
        logger.info(f'{func.__name__} with args {args}')
        for r in func(*args):
            iteration += 1
            logger.info(f'Iteration {iteration} result: {r}')
        return result
    return wrapper


def catch_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            logger.error(f'{func.__name__}: {type(error).__name__}: {error}')
            return None
    return wrapper

@catch_errors
@log_calls
def gen_even_number(n):
    if n < 0:
        raise ValueError('Even number cannot be negative')
    for number in range(0, n+1):
        if number % 2 == 0:
            yield number

@catch_errors
@log_calls
def gen_fibonacci(n):
    if n < 0:
        raise ValueError('Fibonacci number cannot be negative')
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b



class ReverseIterator:
    def __init__(self, data):
        self.data = data
        self.index = len(data)  # начинаем с конца

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]


class EvenIterator:
    def __init__(self, n):
        self.n = n
        self.current = 2

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.n:
            raise StopIteration

        value = self.current
        self.current += 2
        return value





if __name__ == "__main__":
    '''             Логування виконувалось на всіх функціях                 '''
    gen_even_number(20) #перший генератор

    gen_even_number(-10) #перевірка декоратору пошуку помилок

    gen_fibonacci(30) #другий

    gen_fibonacci(-10) #перевірка декоратору шукання помилок

    list_of_int = [1, 2, 3, 4, 5, 10, 30]
    list_with_RI = ReverseIterator(list_of_int) # ітератор ітерується з кінця списку
    reversed_list = [] # створення списку результата ітерацій
    for number in list_with_RI:
        reversed_list.append(number)
    logger.info(f'Reversed list: {reversed_list}')

    integer = EvenIterator(10) # ітератор що ітерується по парних числах від 0 до N
    list_of_even_numbers = [] # створення списку результата ітерацій
    for number in integer:
        list_of_even_numbers.append(number)
    logger.info(f'Even numbers: {list_of_even_numbers}')



