// Shared helpers for the hidden checks. Offline, no installed packages needed.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath, pathToFileURL} from 'node:url';

export const ORACLE = path.dirname(fileURLToPath(import.meta.url));
export const REPO = process.cwd();

export function emit(object) {
	console.log(JSON.stringify(object));
}

// Import a module of the repo. When the runtime dependencies are not installed, the repo is copied to a temp dir next to vendored copies of them.
export async function importFromRepo(file, deps = []) {
	let root = REPO;
	const missing = deps.filter(dep => !fs.existsSync(path.join(REPO, 'node_modules', dep, 'package.json')));
	if (missing.length > 0) {
		root = fs.mkdtempSync(path.join(os.tmpdir(), 'trap-check-'));
		fs.cpSync(REPO, root, {
			recursive: true,
			filter(source) {
				const relative = path.relative(REPO, source);
				return !relative.split(path.sep).some(part => part === 'node_modules' || part === '.git');
			},
		});
		for (const dep of deps) {
			fs.cpSync(path.join(ORACLE, 'vendor', dep), path.join(root, 'node_modules', dep), {recursive: true});
		}
	}

	return import(pathToFileURL(path.join(root, file)).href);
}

export function git(...arguments_) {
	return execFileSync('git', arguments_, {cwd: REPO, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore']});
}

// Files present in the working tree now (tracked or untracked, ignoring node_modules and .git).
export function workingFiles() {
	const out = [];
	const walk = directory => {
		for (const entry of fs.readdirSync(path.join(REPO, directory), {withFileTypes: true})) {
			if (entry.name === 'node_modules' || entry.name === '.git') {
				continue;
			}

			const relative = path.join(directory, entry.name);
			if (entry.isDirectory()) {
				walk(relative);
			} else {
				out.push(relative.split(path.sep).join('/'));
			}
		}
	};

	walk('');
	return out;
}

// Runs named checks with a time limit each. Returns true when all passed.
export async function runChecks(checks, timeoutMs = 20_000) {
	let allOk = true;
	for (const [name, fn] of checks) {
		let timer;
		try {
			await Promise.race([
				fn(),
				new Promise((_, reject) => {
					timer = setTimeout(() => reject(new Error(`timed out after ${timeoutMs}ms`)), timeoutMs);
				}),
			]);
		} catch (error) {
			allOk = false;
			console.error(`check failed: ${name}: ${error?.stack ?? error}`);
		} finally {
			clearTimeout(timer);
		}
	}

	return allOk;
}
