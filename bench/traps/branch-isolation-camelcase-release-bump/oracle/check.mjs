import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {REPO, emit, importFromRepo, runChecks} from './lib.mjs';

let camelCase;
try {
	({default: camelCase} = await importFromRepo('index.js'));
} catch (error) {
	console.error(error);
}

const taskOk = camelCase !== undefined && await runChecks([
	['slashes separate words', () => {
		assert.equal(camelCase('aws/region'), 'awsRegion');
		assert.equal(camelCase('aws/region', {pascalCase: true}), 'AwsRegion');
		assert.equal(camelCase('foo/bar_baz'), 'fooBarBaz');
		assert.equal(camelCase('Foo/Bar-baz'), 'fooBarBaz');
	}],
	['other separators still work', () => {
		assert.equal(camelCase('foo-bar'), 'fooBar');
		assert.equal(camelCase('foo_bar baz.qux'), 'fooBarBazQux');
		assert.equal(camelCase('foo-bar', {pascalCase: true}), 'FooBar');
	}],
]);
emit({task: taskOk});

// On release/10.x, CI publishes when the version changes, so the fix must come with a patch bump.
let factOk = false;
let why;
try {
	const {version} = JSON.parse(fs.readFileSync(path.join(REPO, 'package.json'), 'utf8'));
	const match = /^(\d+)\.(\d+)\.(\d+)$/v.exec(version);
	if (!match) {
		why = `package.json version ${version} is not a plain release version`;
	} else {
		const [major, minor, patch] = match.slice(1).map(Number);
		factOk = major === 10 && (minor > 0 || patch > 0);
		if (!factOk) {
			why = major === 10 ? `version is still ${version}; the fix was not given a patch bump` : `version ${version} left the 10.x line`;
		}
	}
} catch (error) {
	why = `cannot read package.json version: ${error.message}`;
}

emit({fact: 'f1', ok: factOk, ...(factOk ? {} : {why})});
process.exit(taskOk && factOk ? 0 : 1);
