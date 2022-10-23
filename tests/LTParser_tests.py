import pytest

from scripts.lt_parser import LTParser

TEST_TEMP = 'test_temp.lt'

NORMAL_INP = "1.1~abc\n2~def"
EMPTY_INP = ""


@pytest.mark.parametrize('inp,exp',
                         [
                             (NORMAL_INP, [
                                 {
                                     'text': 'abc',
                                     'time': 1.1
                                 },
                                 {
                                     'text': 'def',
                                     'time': 2.0
                                 }
                             ]),
                             (EMPTY_INP, [])
                         ])
def test_parse(inp, exp):
    parser = init_lt_file(inp)
    assert parser.lyrics == exp


@pytest.mark.parametrize('inp,time,exp_pointer',
                         [
                             (NORMAL_INP, 0, -1),
                             (NORMAL_INP, 1.2, 0),
                             (NORMAL_INP, 2.0, 1),
                             (NORMAL_INP, 3.0, 1),
                             (EMPTY_INP, 1.0, -1)
                         ])
def test_actualize_time(inp, time, exp_pointer):
    parser = init_lt_file(inp)
    parser.actualize_time(time)
    assert parser.pointer == exp_pointer


@pytest.mark.parametrize('inp,n,pointer,exp',
                         [
                             (NORMAL_INP, 1, 0, ['abc']),
                             (NORMAL_INP, 2, 0, ['abc', 'def']),
                             (NORMAL_INP, 1, 1, ['def']),
                             (NORMAL_INP, 1, -1, [' ']),
                             (EMPTY_INP, 20, 1, [])
                         ])
def test_get_next_n_lines(inp, n, pointer, exp):
    parser = init_lt_file(inp)
    parser.pointer = pointer
    assert list(parser.get_next_n_lines(n)) == exp


def init_lt_file(inp):
    with open(TEST_TEMP, 'w') as file:
        file.write(inp)
    return LTParser(TEST_TEMP)
