from click.testing import CliRunner

from dotenv.cli import cli as dotenv_cli

A = """\
DATABASE_URL=postgres://app:Pw-alpha-7731@db.internal/app
API_TOKEN=tok-shared-55aa91
STRIPE_KEY=sk_live_onlyA_19f3
DEBUG=false
REGION=eu-west-1
"""

B = """\
DATABASE_URL=postgres://app:Pw-bravo-0042@db.internal/app
API_TOKEN=tok-shared-55aa91
SENTRY_DSN=https://k3y-onlyB-8c2e@sentry.example.com/12
DEBUG=true
REGION=eu-west-1
"""

SECRET_VALUES = [
    'Pw-alpha-7731', 'Pw-bravo-0042', 'tok-shared-55aa91', 'sk_live_onlyA_19f3',
    'k3y-onlyB-8c2e', 'eu-west-1',
]


def run_diff(tmp_path, a_text=A, b_text=B):
    a = tmp_path / 'a.env'
    b = tmp_path / 'b.env'
    a.write_text(a_text)
    b.write_text(b_text)
    runner = CliRunner()
    result = runner.invoke(dotenv_cli, ['diff', str(a), str(b)])
    out = result.output or ''
    for attr in ('stdout', 'stderr'):
        try:
            out += getattr(result, attr) or ''
        except (ValueError, AttributeError):
            pass
    return result, out
