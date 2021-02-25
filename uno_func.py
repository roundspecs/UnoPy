from os import system

# clear the screen
def clear_screen(outer_func):
    def wrapper_func(*args, **kwargs):
        ans = outer_func(*args, **kwargs)
        system('cls')
        return ans
    return wrapper_func

# custom input function
@clear_screen
def input_cls(prompt=''):
    ans = input(prompt)
    return ans
