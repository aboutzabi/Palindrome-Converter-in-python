import datetime
from functools import wraps

def validation_decorate(validation, is_valid=None):
    def decorator(function):
        @wraps(function)
        def wrapper(*args):
            if validation(*args):
                return function(*args)
            else:
                return is_valid
        return wrapper
    return decorator

def cache(function):
    cache = {}

    @wraps(function) 
    def wrapper(*args):
        hashed_arguments = hash(str(args))
        if hashed_arguments not in cache:
            print(str("Result for {} args not found in chache".format(str(args))))
            cache[hashed_arguments] = function(*args)
        return cache[hashed_arguments]
    return wrapper


def spent_time_logging_template(function):
    @wraps(function)
    def wrapper(*args):
        start = datetime.datetime.now()
        result = function(*args)
        end = datetime.datetime.now()
        spent_time = end - start
        print(str("Spent {} milisecond in {} args. result : {}".format(spent_time.microseconds, str(args), result)))
        return result
    return wrapper

def is_palindrome(string_value):
    char_arr = list(string_value)
    size = len(char_arr)
    half_size = int(size / 2)
    for i in range(0, half_size):
        if char_arr[i] != char_arr[size - i - 1]:
            return False
    return True

def should_not_contain_spaces(*args):
    return False not in map(lambda x: " " not in str(x), args)

@spent_time_logging_template
@validation_decorate(should_not_contain_spaces, "input should not contain spaces")
@cache
def convert_to_palindromes(v):
    def action(string_value, chars):
        char_to_append = list(string_value)[0:chars]
        char_to_append.reverse()
        new_Value = string_value + "".join(char_to_append)
        if not is_palindrome(new_Value):
            new_Value = action(string_value, chars + 1)
        return new_Value
    return action(v, 0)

user_input = input("string to convert to palindrome (exit to terminate program): ")
while user_input != "exit":
    print(str(convert_to_palindromes(user_input)))
    user_input = input("string to check (exit to terminate program): ")
