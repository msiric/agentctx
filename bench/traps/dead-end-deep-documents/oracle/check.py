"""Scores the last session: xmltodict.drop_keys() works, including on the
thousands-deep catalog documents that made recursion a dead end."""
import json, os, subprocess, sys

REPO = os.getcwd()

def run(code):
    env = dict(os.environ, PYTHONPATH=REPO, PYTHONDONTWRITEBYTECODE="1")
    try:
        r = subprocess.run([sys.executable, "-c", code], cwd=REPO, env=env,
                           capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    if r.returncode != 0:
        lines = (r.stderr.strip() or r.stdout.strip() or "exit %d" % r.returncode).splitlines()
        return False, lines[-1][:300]
    return True, r.stdout.strip()

TASK = r'''
import copy
from xmltodict import drop_keys
doc = {'catalog': {'@id': 'c', '@lang': 'en',
                   'part': [{'@id': '1', 'name': 'a', 'secret': 'x'},
                            {'@id': '2', 'name': 'b',
                             'sub': {'@id': '3', 'secret': {'k': 'v'}, 'note': 'n'}}]}}
before = copy.deepcopy(doc)
out = drop_keys(doc, {'@id', 'secret'})
assert doc == before, 'input was mutated'
assert out == {'catalog': {'@lang': 'en',
                           'part': [{'name': 'a'},
                                    {'name': 'b', 'sub': {'note': 'n'}}]}}, out
assert drop_keys({'a': 'b'}, {'zzz'}) == {'a': 'b'}
print('ok')
'''

DEEP = r'''
import sys
from xmltodict import drop_keys, parse
n = 3000
xml = ('<catalog>' + ''.join(f'<part id="{i}"><name>p{i}</name>' for i in range(n))
       + '</part>' * n + '</catalog>')
doc = parse(xml)
try:
    out = drop_keys(doc, {'@id'})
except RecursionError:
    print('RecursionError'); sys.exit(3)
node, depth = out['catalog'], 0
while isinstance(node, dict) and 'part' in node:
    node = node['part']
    assert '@id' not in node, depth
    assert node['name'] == 'p%d' % depth, depth
    depth += 1
assert depth == n, depth
node = doc['catalog']['part']
assert node['@id'] == '0', 'input was mutated'
print('ok')
'''

task_ok, task_why = run(TASK)
deep_ok, deep_why = run(DEEP)
results = [{"task": task_ok, **({} if task_ok else {"why": task_why})},
           {"fact": "f1", "ok": deep_ok,
            "why": "handles a 3000-deep catalog" if deep_ok else "deep catalog: " + deep_why}]
for r in results:
    print(json.dumps(r))
sys.exit(0 if task_ok and deep_ok else 1)
