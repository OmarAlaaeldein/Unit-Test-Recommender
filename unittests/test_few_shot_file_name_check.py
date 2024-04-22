from file_name_check import file_name_check
import pytest

@pytest.mark.parametrize('filename, expected_result', [
    ("example.txt", "Yes"),
    ("1example.dll", "No"),
    ("hello.exe", "Yes"),
    ("myprogram.dll", "Yes"),
    ("thisisaverylongfilenamethatshouldnotbevalid.doc", "No"),
    ("noextension", "No"),
    ("toomanyextentions.txt.pdf", "No"),
    ("threedigitsinfront007.txt", "Yes"),
    ("morethanthreedigitsinthebeginning0008564.txt", "No"),
    ("emptystringbeforeperiod..txt", "No"),
    ("onlyonedot.txt.", "No"),
    ("twoconsecutivedots...txt", "No"),
    ("multipledotsseparatedbydigits1.2.3.txt", "No"),
    ("endingwithaunderscore.txt_", "No"),
    ("havingbothalphanumericandspecialchars.txt?/<>\\|[]{}", "No"),
    ("havingbothalphanumericspecialcharsanddots.txt?./<>.???", "No"),
    ])
def test_file_name_check(filename, expected_result):
    actual_result = file_name_check(filename)
    assert actual_result == expected_result, f"Expected {expected_result} but got {actual_result}"