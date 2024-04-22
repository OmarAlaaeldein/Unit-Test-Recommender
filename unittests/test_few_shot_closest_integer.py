import pytest
from closest_integer import closest_integer

@pytest.mark.parametrize('input_, expected', [
    ('10', 10),
    ('14.9', 15),
    ('17.6', 18),
])
def test_positive_cases(input_, expected):
    result = closest_integer(input_)
    assert result == expected

@pytest.mark.parametrize('input_, expected', [
    ('-10', -10),
    ('-14.9', -15),
    ('-17.6', -18),
])
def test_negative_cases(input_, expected):
    result = closest_integer(input_)
    assert result == expected

@pytest.mark.parametrize('input_, expected', [
    ('14.5', 15),
    ('-14.5', -15),
    ('14.4', 14),
    ('-14.4', -14),
])
def test_tiebreaker_away_zero(input_, expected):
    result = closest_integer(input_)
    assert result == expected
