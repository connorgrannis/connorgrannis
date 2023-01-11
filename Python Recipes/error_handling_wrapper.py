def log_it(f):
    """ will decorate a function with error handling """
    def logging_exceptions(*args, **kwargs):
        """ tries a function. If there's a problem, it returns None """
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Problem!!\n {e}")
            return None
    return logging_exceptions


@log_it
def error(err=True):
    if err:
        raise NameError
    else:
        return "All good"

print(error(True) )
print(error(False))
