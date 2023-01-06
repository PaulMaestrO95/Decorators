import pathlib
import types

from path_logger import logger

path = pathlib.Path('main.log')


@logger(path)
def flat_generator_2(list_of_lists):
    for i in list_of_lists:
        if isinstance(i, list):
            yield from flat_generator_2(i)
        else:
            yield i


@logger(path)
def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator_2(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator_2(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator_2(list_of_lists_2), types.GeneratorType)
