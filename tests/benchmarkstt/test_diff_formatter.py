import benchmarkstt.diff.formatter as formatter
import pytest

a = 'ABCDEFGHJKLMN'
b = 'ABBCDEFHHIJKLM'


@pytest.mark.parametrize('dialect,expected', [
    ['text', 'AB\u0359BCDEFG\u0338HH\u0359I\u0359JKLMN\u0338'],
    ['cli', 'A\033[32mB\033[0mBCDEF\033[31mG\033[0mH\033[32mHI\033[0mJKLM\033[31mN\033[0m'],
    ['html', 'A<span class="insert">B</span>BCDEF<span class="delete">G</span>'
             'H<span class="insert">HI</span>JKLM<span class="delete">N</span>'],
    ['json', '['
             '{"kind": "equal", "reference": "A", "hypothesis": "A"}, '
             '{"kind": "insert", "reference": null, "hypothesis": "B"}, '
             '{"kind": "equal", "reference": "BCDEF", "hypothesis": "BCDEF"}, '
             '{"kind": "delete", "reference": "G", "hypothesis": null}, '
             '{"kind": "equal", "reference": "H", "hypothesis": "H"}, '
             '{"kind": "insert", "reference": null, "hypothesis": "HI"}, '
             '{"kind": "equal", "reference": "JKLM", "hypothesis": "JKLM"}, '
             '{"kind": "delete", "reference": "N", "hypothesis": null}'
             ']'],
])
def test_format_diff(dialect, expected):
    gotten = formatter.format_diff(a, b, dialect=dialect)
    assert gotten == expected


def test_no_diff():
    assert formatter.format_diff(a, a, dialect='cli') == a


def test_dialect_formatters():
    with pytest.raises(NotImplementedError):
        formatter.Dialect.format(None, None)

    assert formatter.UTF8Dialect().format(['a', 'b'], 'diff') == 'a|b: diff'


def test_dialect_exceptions():
    with pytest.raises(ValueError) as exc:
        formatter.DiffFormatter(dialect='dialectdoesntexist')
    assert 'Unknown diff dialect' in str(exc)


def test_default_dialect():
    assert formatter.DiffFormatter().diff(a, b) == formatter.format_diff(a, b)
