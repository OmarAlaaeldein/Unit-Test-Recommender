from file_name_check import file_name_check
import pytest

@pytest.mark.parametrize('filename, expected', [
    ("example.txt", "Yes"),
    ("1example.dll", "No"),
    ("hello.exe", "Yes"),
    ("myprogram.dll", "Yes"),
    ("thisisaverylongfilenamethatshouldnotbevalid.doc", "No"),
    ("456789abcde.pdf", "No"),
    ("123.jpg", "No"),
    ("noextension", "No"),
    ("empty.", "No"),
    (".hidden", "No"),
    ("invalidsuffix.png", "No"),
    ("invalidcharacters!#$.dat", "No"),
])
def test_file_name_check(filename, expected):
    assert file_name_check(filename) == expected