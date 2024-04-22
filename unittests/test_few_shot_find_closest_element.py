from typing import List, Optional, Tuple
from find_closest_elements import find_closest_elements


def test_find_closest_elements():
    numbers = [1.0, 2.0, 3.0, 4.0, 5.0, 2.2]
    output = find_closest_elements(numbers)
    expected_output = (2.0, 2.2)
    assert output == expected_output