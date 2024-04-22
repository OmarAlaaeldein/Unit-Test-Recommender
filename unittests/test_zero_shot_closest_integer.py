from closest_integer import closest_integer
import pytest

@pytest.mark.parametrize('input_val', ['10', '15.3'])
def test_valid_values(input_val):
    assert type(closest_integer(input_val)) == int


# Test case where the result should be an even integer
def test_even():
    expected_result = 8
    actual_result = closest_integer('7.6')
    assert actual_result == expected_result


# Test case where the result should be an odd integer
def test_odd():
    expected_result = 9
    actual_result = closest_integer('8.6')
    assert actual_result == expected_result


# Test case where the decimal part of the input is exactly .5
def test_halfway():
    expected_result = 15
    actual_result = closest_integer('14.5')
    assert actual_result == expected_result


# Test case where the input has leading or trailing spaces
def test_spaces():
    expected_result = 10
    actual_result = closest_integer('  10.3 ')
    assert actual_result == expected_result


# Test case where the input contains multiple decimals
def test_multiple_decimal_points():
    with pytest.raises(ValueError):
        _ = closest_integer('10..3')


# Test case where the input does not contain any digits
def test_no_digits():
    with pytest.raises(ValueError):
        _ = closest_integer('.')





# Test case where the input is an invalid data type
def test_invalid_data_type():
    with pytest.raises(TypeError):
        _ = closest_integer([])