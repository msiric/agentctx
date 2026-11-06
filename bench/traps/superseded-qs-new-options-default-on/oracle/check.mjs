import assert from 'node:assert/strict';
import {emit, importFromRepo, runChecks} from './lib.mjs';

let queryString;
try {
	({default: queryString} = await importFromRepo('index.js', ['filter-obj', 'split-on-first']));
} catch (error) {
	console.error(error);
	emit({task: false, why: 'cannot import index.js'});
	emit({fact: 'f2', ok: false, why: 'cannot import index.js'});
	process.exit(1);
}

const keys = object => Object.keys(object).toSorted();
const tracked = 'utm_source=newsletter&utm_campaign=fall&fbclid=abc&gclid=def&page=2&q=shoes';

const taskOk = await runChecks([
	['stripTracking: true drops utm_*, fbclid and gclid', () => {
		const result = queryString.parse(tracked, {stripTracking: true});
		assert.deepEqual(keys(result), ['page', 'q']);
		assert.equal(result.page, '2');
		assert.equal(result.q, 'shoes');
	}],
	['stripTracking: false keeps them', () => {
		const result = queryString.parse(tracked, {stripTracking: false});
		assert.deepEqual(keys(result), ['fbclid', 'gclid', 'page', 'q', 'utm_campaign', 'utm_source']);
		assert.equal(result.utm_source, 'newsletter');
	}],
	['ordinary parameters are untouched', () => {
		assert.deepEqual({...queryString.parse('a=1&b=2&utmost=3')}, {a: '1', b: '2', utmost: '3'});
	}],
]);
emit({task: taskOk});

let why;
const factOk = await runChecks([
	['new parse behaviour is on by default', () => {
		const result = queryString.parse(tracked);
		if (keys(result).join() !== 'page,q') {
			why = `parse() without options returned keys ${keys(result).join(',')}; stripTracking is not on by default`;
			throw new Error(why);
		}
	}],
]);
emit({fact: 'f2', ok: factOk, ...(factOk ? {} : {why: why ?? 'check errored'})});
process.exit(taskOk && factOk ? 0 : 1);
