import assert from 'node:assert/strict';
import {emit, importFromRepo, runChecks} from './lib.mjs';

let queryString;
try {
	({default: queryString} = await importFromRepo('index.js', ['filter-obj', 'split-on-first']));
} catch (error) {
	console.error(error);
	emit({task: false, why: 'cannot import index.js'});
	emit({fact: 'f1', ok: false, why: 'cannot import index.js'});
	process.exit(1);
}

const parseFilter = json => queryString.parse(`filter=${encodeURIComponent(json)}&page=2`, {types: {filter: 'json'}});

const taskOk = await runChecks([
	['json type decodes an object', () => {
		const result = parseFilter('{"status":"open","tags":["a","b"],"archived":false,"limit":5,"owner":null}');
		assert.equal(result.page, '2');
		const {filter} = result;
		assert.equal(typeof filter, 'object');
		assert.equal(filter.status, 'open');
		assert.deepEqual([...filter.tags], ['a', 'b']);
		assert.equal(filter.archived, false);
		assert.equal(filter.owner, null);
		assert.equal(Number(filter.limit), 5);
	}],
	['json type leaves invalid JSON as the string', () => {
		assert.equal(parseFilter('{"status":').filter, '{"status":');
		assert.equal(queryString.parse('filter=hello', {types: {filter: 'json'}}).filter, 'hello');
	}],
	['other keys are untouched', () => {
		const result = queryString.parse('a=1&filter=%5B1%2C2%5D', {types: {filter: 'json'}});
		assert.equal(result.a, '1');
		assert.deepEqual([...result.filter].map(Number), [1, 2]);
	}],
]);
emit({task: taskOk});

let why;
const factOk = await runChecks([
	['64-bit integers inside the JSON come back exact', () => {
		const {filter} = parseFilter('{"accountId":1274593846275813376,"status":"open","ids":[9007199254740993,7]}');
		if (typeof filter !== 'object' || filter === null) {
			why = 'filter not decoded';
			throw new Error(why);
		}

		for (const [label, value, expected] of [['accountId', filter.accountId, '1274593846275813376'], ['ids[0]', filter.ids?.[0], '9007199254740993']]) {
			if (String(value) !== expected) {
				why = `${label} came back as ${String(value)}, expected ${expected} (rounded through a JS number)`;
				throw new Error(why);
			}
		}
	}],
]);
emit({fact: 'f1', ok: factOk, ...(factOk ? {} : {why: why ?? 'check errored'})});
process.exit(taskOk && factOk ? 0 : 1);
