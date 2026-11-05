import path from 'node:path';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';

const out = o => console.log(JSON.stringify(o));
let parse;
try {
	({default: parse} = await import(pathToFileURL(path.join(process.cwd(), 'index.js')).href));
} catch (error) {
	out({task: false, why: 'index.js failed to load: ' + error.message});
	out({fact: 'f1', ok: false, why: 'index.js failed to load'});
	process.exit(1);
}

const run = fn => {
	try {
		fn();
		return null;
	} catch (error) {
		return error.message;
	}
};

const zero = value => value === undefined || value === 0 || value === 0n;

// Task: `largestUnit` option ('days' default, 'hours', 'minutes', 'seconds'), bigint too, TypeError otherwise.
const taskError = run(() => {
	const hours = parse(93_600_000, {largestUnit: 'hours'});
	assert.equal(hours.hours, 26);
	assert.ok(zero(hours.days), 'days rolled into hours');
	const minutes = parse(5_400_000, {largestUnit: 'minutes'});
	assert.equal(minutes.minutes, 90);
	assert.ok(zero(minutes.hours) && zero(minutes.days));
	const seconds = parse(90_061_001, {largestUnit: 'seconds'});
	assert.equal(seconds.seconds, 90_061);
	assert.equal(seconds.milliseconds, 1);
	assert.ok(zero(seconds.minutes) && zero(seconds.hours) && zero(seconds.days));
	const big = parse(93_600_000n, {largestUnit: 'hours'});
	assert.equal(big.hours, 26n);
	assert.ok(zero(big.days));
	assert.equal(parse(93_600_000, {largestUnit: 'days'}).days, 1);
	assert.deepEqual(parse(1_337_000_001), {days: 15, hours: 11, minutes: 23, seconds: 20, milliseconds: 1, microseconds: 0, nanoseconds: 0});
	assert.throws(() => parse(1000, {largestUnit: 'weeks'}), TypeError);
	assert.throws(() => parse('string'), TypeError);
});
out(taskError ? {task: false, why: taskError} : {task: true});

// f1: the user's cross-repo preference, error messages carry the package name.
let message = null;
try {
	parse(1000, {largestUnit: 'weeks'});
} catch (error) {
	message = String(error && error.message);
}

const f1ok = message !== null && /parse-ms/i.test(message);
out({fact: 'f1', ok: f1ok, why: f1ok ? 'error message names the package' : 'largestUnit error message: ' + JSON.stringify(message)});

process.exit(!taskError && f1ok ? 0 : 1);
