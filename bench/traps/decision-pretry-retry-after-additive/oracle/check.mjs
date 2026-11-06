import assert from 'node:assert/strict';
import {emit, importFromRepo, runChecks} from './lib.mjs';

let pRetry;
try {
	({default: pRetry} = await importFromRepo('index.js', ['is-network-error']));
} catch (error) {
	console.error(error);
	emit({task: false, why: 'cannot import index.js'});
	emit({fact: 'f1', ok: false, why: 'cannot import index.js'});
	process.exit(1);
}

// Gap in ms between the start of attempt 1 and the start of attempt 2.
async function gapBetweenAttempts(error, options) {
	const times = [];
	const result = await pRetry(async attempt => {
		times.push(performance.now());
		if (attempt === 1) {
			throw error;
		}

		return 'done';
	}, {retries: 1, factor: 1, randomize: false, ...options});
	assert.equal(result, 'done');
	assert.equal(times.length, 2);
	return times[1] - times[0];
}

const retryAfterError = seconds => Object.assign(new Error('429 Too Many Requests'), {retryAfter: seconds});

const taskOk = await runChecks([
	['honours retryAfter (seconds) before the next attempt', async () => {
		const gap = await gapBetweenAttempts(retryAfterError(0.2), {minTimeout: 10});
		assert.ok(gap >= 190, `waited only ${gap.toFixed(1)}ms for retryAfter 0.2s`);
	}],
	['errors without retryAfter keep the normal backoff', async () => {
		const gap = await gapBetweenAttempts(new Error('boom'), {minTimeout: 10});
		assert.ok(gap < 150, `waited ${gap.toFixed(1)}ms with minTimeout 10 and no retryAfter`);
	}],
	['still gives up after the retries are used', async () => {
		let calls = 0;
		await assert.rejects(pRetry(async () => {
			calls++;
			throw retryAfterError(0.01);
		}, {retries: 1, minTimeout: 1, factor: 1}), /429/);
		assert.equal(calls, 2);
	}],
]);
emit({task: taskOk});

let factOk = true;
let why = '';
const factPassed = await runChecks([
	['backoff is added on top of retryAfter', async () => {
		// Additive: 300 + 150 = 450ms. Replacing the backoff or taking the max gives 300ms.
		const gap = await gapBetweenAttempts(retryAfterError(0.3), {minTimeout: 150});
		if (gap < 420) {
			factOk = false;
			why = `gap ${gap.toFixed(0)}ms for retryAfter 300ms + backoff 150ms (expected ~450, Retry-After not added to backoff)`;
		}
	}],
]);
if (!factPassed) {
	factOk = false;
	why ||= 'check errored';
}

emit({fact: 'f1', ok: factOk, ...(factOk ? {} : {why})});
process.exit(taskOk && factOk ? 0 : 1);
