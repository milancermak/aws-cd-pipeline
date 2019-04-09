import collections

from src.hello_world import main


Context = collections.namedtuple('Context', ['function_name',
                                             'function_version',
                                             'invoked_function_arn'])


def test_handler():
    context = Context('testname',
                      'testversion',
                      'test:arn')
    result = main.handler({}, context)
    assert result
