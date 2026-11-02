// Lets Node's built-in TypeScript type stripping load sources that use
// extensionless relative imports (`./util`), as TS projects usually do.
const RETRY = new Set(['ERR_MODULE_NOT_FOUND', 'ERR_UNSUPPORTED_DIR_IMPORT']);

export async function resolve(specifier, context, next) {
  try {
    return await next(specifier, context);
  } catch (err) {
    if (!RETRY.has(err?.code) || !/^\.\.?\//.test(specifier) || !context.parentURL?.endsWith('.ts')) throw err;
    for (const candidate of [`${specifier}.ts`, specifier.replace(/\.js$/, '.ts'), `${specifier}/index.ts`]) {
      try {
        return await next(candidate, context);
      } catch {}
    }
    throw err;
  }
}
