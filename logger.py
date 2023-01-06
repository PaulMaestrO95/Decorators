import os
from datetime import datetime
import json

def logger(old_function):
    def new_function(*args, **kwargs):
        time = datetime.now()
        result = old_function(*args, **kwargs)
        log = {}
        log["Date"] = str(time.date())
        log["Time"] = str(time.hour) + ':' + str(time.minute) + ':' + str(time.second)
        log["Function_name"] = old_function.__name__
        log["args"] = args
        log["kwargs"] = kwargs
        log["Result"] = result
        with open("main.log", 'a+', encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False)
            f.write('\n')

        return result

    return new_function

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'