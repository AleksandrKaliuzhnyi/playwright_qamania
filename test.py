

def test_get_answer(answer):
    assert 42 == answer


def test_get_new_answer(new_answer):
    assert 43 == new_answer


def test_get_answers(answer, new_answer):
    assert 42 + 43 == answer + new_answer


def test_native(request):
    assert 'test.py' == request.fspath.basename
