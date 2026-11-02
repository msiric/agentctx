import pytest
from click.testing import CliRunner

from dotenv.cli import cli as dotenv_cli

CONTENT = 'A=1\nEMPTY=\nBARE\nSPACED="a b"\n'


@pytest.fixture
def env_file(tmp_path):
    p = tmp_path / '.env'
    p.write_text(CONTENT)
    return str(p)


def get(env_file, *args):
    return CliRunner().invoke(dotenv_cli, ['--file', env_file, 'get', *args])


@pytest.mark.parametrize('args,code,output', [
    (['A'], 0, '1\n'),
    (['A', '--default', 'x'], 0, '1\n'),
    (['SPACED', '--default', 'x'], 0, 'a b\n'),
    (['MISSING', '--default', 'fallback'], 0, 'fallback\n'),
    (['BARE', '--default', 'fallback'], 0, 'fallback\n'),
    (['EMPTY', '--default', 'fallback'], 0, '\n'),
    (['EMPTY'], 0, '\n'),
    (['MISSING', '--default', ''], 0, '\n'),
])
def test_get_with_default(env_file, args, code, output):
    r = get(env_file, *args)
    assert (r.exit_code, r.output) == (code, output)


@pytest.mark.parametrize('key', ['MISSING', 'BARE'])
def test_get_without_default_still_fails(env_file, key):
    r = get(env_file, key)
    assert r.exit_code == 1
    assert r.output == ''
