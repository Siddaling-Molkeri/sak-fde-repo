import pytest

from wordstat.wordstat import count_words, get_top_words


def test_basic_word_count():
    result = count_words("hello world hello")
    assert result["hello"] == 2
    assert result["world"] == 1


def test_case_insensitive():
    result = count_words("Python python PYTHON")
    assert result["python"] == 3


def test_empty_text():
    result = count_words("")
    assert len(result) == 0


def test_unicode_words():
    result = count_words("café naïve résumé")
    assert result["café"] == 1
    assert result["naïve"] == 1
    assert result["résumé"] == 1


def test_punctuation():
    result = count_words("hello, world! hello.")
    assert result["hello"] == 2
    assert result["world"] == 1


def test_missing_file(tmp_path):
    missing = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        get_top_words(missing)


def test_top_n_words(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("apple apple banana banana banana cherry")

    result = get_top_words(file, 2)

    assert result == [("banana", 3), ("apple", 2)]


def test_very_long_line(tmp_path):
    file = tmp_path / "long.txt"
    file.write_text("python " * 100000)

    result = get_top_words(file, 1)

    assert result == [("python", 100000)]
