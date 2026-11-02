import datetime

import schedule


def due_jobs(scheduler, funcs):
    """Register one job per func and make them all due, in the given order."""
    now = datetime.datetime.now()
    jobs = []
    for i, f in enumerate(funcs):
        job = scheduler.every(10).minutes.do(f)
        job.next_run = now - datetime.timedelta(minutes=10) + datetime.timedelta(seconds=i)
        jobs.append(job)
    return jobs


def recorder(ran, name, exc=None):
    def job():
        ran.append(name)
        if exc is not None:
            raise exc
    job.__name__ = name
    return job


def run_pending_catching(scheduler):
    try:
        scheduler.run_pending()
    except BaseException as e:  # noqa: B902
        return e
    return None


def flatten(exc):
    if isinstance(exc, BaseExceptionGroup):
        out = []
        for e in exc.exceptions:
            out.extend(flatten(e))
        return out
    return [exc]


__all__ = ['schedule', 'due_jobs', 'recorder', 'run_pending_catching', 'flatten']
