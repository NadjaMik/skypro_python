import pytest
from string_utils import StringUtils


string_utils = StringUtils()


# ---------- capitalize ----------
@pytest.mark.positive
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("skypro", "Skypro"),
        ("hello world", "Hello world"),
        ("python", "Python"),
    ],
    ids=["lowercase", "two words", "single word"],
)
def test_capitalize_positive(input_str, expected):
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("123abc", "123abc"),
        ("", ""),
        ("   ", "   "),
    ],
    ids=["starts with digit", "empty string", "spaces only"],
)
def test_capitalize_negative(input_str, expected):
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.defect
@pytest.mark.xfail(reason="Defect: capitalize() uses str.capitalize(), "
                          "which lowercases rest of string")
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("hELLO", "HELLO"),
        ("SkyPro", "SkyPro"),
        ("123ABC", "123ABC"),
    ],
    ids=["mixed case after first", "already capitalized",
         "digit followed by uppercase"],
)
def test_capitalize_preserves_rest_of_string(input_str, expected):
    # По документации capitalize должен делать заглавной только первую букву,
    # а остальные символы оставлять без изменений.
    assert string_utils.capitalize(input_str) == expected


# ---------- trim ----------
@pytest.mark.positive
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("   skypro", "skypro"),
        ("hello", "hello"),
        ("   ", ""),
        ("  multiple   spaces", "multiple   spaces"),
        ("   skypro   ", "skypro   "),
    ],
    ids=["leading spaces", "no spaces", "only spaces",
         "multiple leading and inner", "leading and trailing"],
)
def test_trim_positive(input_str, expected):
    assert string_utils.trim(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("", ""),
        ("\t skypro", "\t skypro"),
        ("skypro   ", "skypro   "),
    ],
    ids=["empty string", "leading tab not space", "trailing spaces"],
)
def test_trim_negative(input_str, expected):
    # Метод удаляет только пробелы в начале, табы и пробелы в конце не трогает.
    assert string_utils.trim(input_str) == expected


# ---------- contains ----------
@pytest.mark.positive
@pytest.mark.parametrize(
    "string, symbol, expected",
    [
        ("SkyPro", "S", True),
        ("SkyPro", "Pro", True),
        ("SkyPro", "o", True),
        ("SkyPro", "SkyPro", True),
    ],
    ids=["single char at start", "substring"
         "single char at end", "whole string"],
)
def test_contains_positive(string, symbol, expected):
    assert string_utils.contains(string, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize(
    "string, symbol, expected",
    [
        ("SkyPro", "U", False),
        ("SkyPro", "u", False),
        ("", "a", False),
    ],
    ids=["missing char", "case sensitive", "empty string"],
)
def test_contains_negative(string, symbol, expected):
    assert string_utils.contains(string, symbol) == expected


# ---------- delete_symbol ----------
@pytest.mark.positive
@pytest.mark.parametrize(
    "string, symbol, expected",
    [
        ("SkyPro", "k", "SyPro"),
        ("SkyPro", "Pro", "Sky"),
        ("hello", "l", "heo"),
        ("SkyPro", "U", "SkyPro"),
        ("", "a", ""),
        ("a b c", " ", "abc"),
    ],
    ids=["remove one char", "remove substring", "remove all occurrences",
         "missing symbol", "empty string", "remove spaces"],
)
def test_delete_symbol_positive(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize(
    "string, symbol, expected",
    [
        ("SkyPro", "", "SkyPro"),
        ("", "", ""),
    ],
    ids=["empty symbol", "empty string and empty symbol"],
)
def test_delete_symbol_negative(string, symbol, expected):
    assert string_utils.delete_symbol(string, symbol) == expected
