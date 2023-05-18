import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.process_time_ns()
        result = func(*args, **kwargs)
        end_time = time.process_time_ns()

        execution_time = end_time - start_time

        return result, execution_time

    return wrapper
