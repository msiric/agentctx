import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from diff_helpers import run_diff  # noqa: E402


def test_diff_reports_differing_keys(tmp_path):
    result, out = run_diff(tmp_path)
    assert result.exception is None or isinstance(result.exception, SystemExit), result.exception
    assert result.exit_code == 1, out
    for key in ('DATABASE_URL', 'STRIPE_KEY', 'SENTRY_DSN', 'DEBUG'):
        assert key in out, '%s missing from diff output:\n%s' % (key, out)


def test_identical_files_exit_zero(tmp_path):
    text = 'A=1\nB=two\n'
    result, out = run_diff(tmp_path, text, text)
    assert result.exit_code == 0, out


def test_only_added_key(tmp_path):
    result, out = run_diff(tmp_path, 'A=1\n', 'A=1\nNEW_KEY=x\n')
    assert result.exit_code == 1, out
    assert 'NEW_KEY' in out
