import datetime

import schedule


def make_due(jobs):
    now = datetime.datetime.now()
    for i, job in enumerate(jobs):
        job.next_run = now - datetime.timedelta(minutes=5) + datetime.timedelta(seconds=i)


def rec(ran, name):
    def job():
        ran.append(name)
    job.__name__ = name
    return job


def test_pause_skips_tagged_jobs_and_resume_restores_them():
    s = schedule.Scheduler()
    ran = []
    a = s.every(10).minutes.do(rec(ran, 'a')).tag('maint')
    b = s.every(10).minutes.do(rec(ran, 'b')).tag('maint', 'other')
    c = s.every(10).minutes.do(rec(ran, 'c')).tag('other')
    d = s.every(10).minutes.do(rec(ran, 'd'))

    s.pause('maint')
    make_due([a, b, c, d])
    s.run_pending()
    assert sorted(ran) == ['c', 'd']

    # still paused on later ticks
    make_due([a, b])
    s.run_pending()
    assert sorted(ran) == ['c', 'd']
    assert len(s.get_jobs()) == 4, 'pausing must not cancel jobs'

    s.resume('maint')
    make_due([a, b])
    s.run_pending()
    assert sorted(ran) == ['a', 'b', 'c', 'd']


def test_pause_is_per_scheduler():
    s1, s2 = schedule.Scheduler(), schedule.Scheduler()
    ran = []
    j1 = s1.every().minute.do(rec(ran, 'one')).tag('maint')
    j2 = s2.every().minute.do(rec(ran, 'two')).tag('maint')
    s1.pause('maint')
    make_due([j1, j2])
    s1.run_pending()
    s2.run_pending()
    assert ran == ['two']


def test_resume_unknown_tag_is_harmless():
    s = schedule.Scheduler()
    ran = []
    j = s.every().minute.do(rec(ran, 'x'))
    s.resume('nope')
    make_due([j])
    s.run_pending()
    assert ran == ['x']
