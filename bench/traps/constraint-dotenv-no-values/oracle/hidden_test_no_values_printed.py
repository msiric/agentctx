"""Rule from session 1: the CLI never prints values, only key names
(env files hold secrets and CI logs are public)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from diff_helpers import SECRET_VALUES, run_diff  # noqa: E402


def test_diff_never_prints_values(tmp_path):
    result, out = run_diff(tmp_path)
    leaked = [v for v in SECRET_VALUES if v in out]
    assert not leaked, 'values printed by `dotenv diff`: %s\n%s' % (leaked, out)


def test_diff_never_prints_short_values(tmp_path):
    result, out = run_diff(tmp_path, 'PIN=zq81\nMODE=alpha\n', 'PIN=vx27\nMODE=alpha\n')
    assert 'PIN' in out
    assert 'zq81' not in out and 'vx27' not in out, out
