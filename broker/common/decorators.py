from termcolor import colored, cprint


def private_api(func):
    def wrapper(*args, **kwargs):
        funcname = colored(func.__name__, "yellow", attrs=["bold"])
        cprint(f"CALLING a private API {funcname}", attrs=["bold"])
        result = func(*args, **kwargs)
        return result

    return wrapper


def public_api(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapper
