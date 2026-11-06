import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {REPO, emit, git, importFromRepo, runChecks, workingFiles} from './lib.mjs';

const PINNED = '48866469ca1793e1f163a964fc77e839f5038a3f';

let module_;
try {
	module_ = await importFromRepo('index.js');
} catch (error) {
	console.error(error);
}

const taskOk = module_ !== undefined && await runChecks([
	['decamelizeKeys is a named export and the default export still works', () => {
		assert.equal(typeof module_.decamelizeKeys, 'function');
		assert.equal(module_.default('unicornRainbow'), 'unicorn_rainbow');
	}],
	['decamelizes own keys, shallow, values untouched', () => {
		const nested = {innerKey: 2};
		const input = {fooBar: 1, bazQux: nested, already_snake: 'x'};
		const output = module_.decamelizeKeys(input);
		assert.deepEqual({...output}, {foo_bar: 1, baz_qux: {innerKey: 2}, already_snake: 'x'});
		assert.equal(output.baz_qux, nested);
		assert.deepEqual(Object.keys(input), ['fooBar', 'bazQux', 'already_snake']);
	}],
	['passes options through', () => {
		assert.deepEqual({...module_.decamelizeKeys({fooBar: 1}, {separator: '-'})}, {'foo-bar': 1});
		assert.deepEqual({...module_.decamelizeKeys({testGUILabel: 1}, {preserveConsecutiveUppercase: true})}, {test_GUI_label: 1});
	}],
]);
emit({task: taskOk});

// The user's preference: tests for new work go in a new test file, never appended to an existing one.
let factOk = true;
let why;
try {
	if (git('diff', PINNED, '--', 'test.js').trim() !== '') {
		factOk = false;
		why = 'tests were added to the existing test.js';
	} else {
		const pinnedFiles = new Set(git('ls-tree', '-r', '--name-only', PINNED).split('\n').filter(Boolean));
		const newTestFiles = workingFiles()
			.filter(file => !pinnedFiles.has(file) && /\.(?:[cm]?js|[cm]?ts)$/v.test(file) && /test|spec/iv.test(file))
			.filter(file => fs.readFileSync(path.join(REPO, file), 'utf8').includes('decamelizeKeys'));
		if (newTestFiles.length === 0) {
			factOk = false;
			why = 'no new test file covering decamelizeKeys';
		}
	}
} catch (error) {
	factOk = false;
	why = `could not inspect files: ${error.message}`;
}

emit({fact: 'f1', ok: factOk, ...(factOk ? {} : {why})});
process.exit(taskOk && factOk ? 0 : 1);
