def total_sum(masiv):
    return sum(int(x) for x in masiv.split(","))

def get_area(width, height):
    return width * height

def get_perimeter(width, height):
    return 2 * (width + height)


def unique_symb_check(set1):
    set1 = set(set1)
    if len(set1) > 10:
        return True
    else:
        return False

def find_str(list_of_something):
    result = list_of_something = [x for x in list_of_something if type(x) is str]
    return result

def the_longest(list1):
    list1.sort(key=len)
    return list1[-1]

def tipa_reverse(string):
    string = string[::-1]
    return string


def serednie_arifmet(list1):
    return sum(list1) // len(list1)


def validate_password(password: str):
    """Проверяет пароль и возвращает список найденных проблем.

    Правила:
      - минимум 8 символов;
      - хотя бы одна заглавная буква;
      - хотя бы одна строчная буква;
      - хотя бы одна цифра;
      - нет пробелов.

    """
    problems = []

    if len(password) < 8:
        problems.append("слишком короткий (меньше 8 символов)")
    if not any(char.isupper() for char in password):
        problems.append("нет заглавной буквы")
    if not any(char.islower() for char in password):
        problems.append("нет строчной буквы")
    if not any(char.isdigit() for char in password):
        problems.append("нет цифры")
    if any(char.isspace() for char in password):
        problems.append("содержит пробелы")

    return problems


def is_palindrome(number):
    strNumber = str(number)
    if strNumber == strNumber[::-1]:
        return 'Is palindrome'
    else:
        return f'{number} is not palindrome'

