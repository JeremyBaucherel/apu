# -*- coding: iso-8859-1 -*-


"""Utilities to help dealing with date and times."""


import calendar
import datetime

MONTH_NAMES = [u"Janvier", u"F\xe9vrier", u"Mars", u"Avril", u"Mai", u"Juin", u"Juillet", u"Août", u"Septembre", u"Octobre", u"Novembre", u"D\xe9cembre"]
MONTH_SHORT_NAMES = [u"Jan.", u"F\xe9v.", u"Mar.", u"Avr.", u"Mai", u"Juin", u"Juil.", u"Août", u"Sep.", u"Oct.", u"Nov.", u"D\xe9c."]
MONTH_SHORT_NAMES_EN = [u"Jan.", u"Feb.", u"Mar.", u"Apr.", u"May", u"June", u"July", u"Aug.", u"Sep.", u"Oct.", u"Nov.", u"Dec."]


class DayRange (object):
    """
    List each day between two dates. Start and end dates are included (inclusive interval).

    >>> for day in apu.dt.MonthRange(datetime.date(2020, 2, 1), datetime.date(2020, 2, 3)):
    >>>    print(day)
    2020-02-01
    2020-02-02
    2020-02-03
    """

    def __init__ (self, start_date, end_date):
        assert start_date
        assert end_date

        self.start = start_date
        self.end = end_date

    def __iter__ (self):
        return DayRangeIterator(self.start, self.end)
		

class DayRangeIterator (object):

    def __init__ (self, start_date, end_date):
        self.start = start_date
        self.end = end_date
        self._current_day = self.start

    def __iter__ (self):
        return self

    def __next__ (self):
        date = self._current_day
        if date > self.end:
            raise StopIteration()
        self._current_day += datetime.timedelta(days=1)
        return date
       
    next = __next__


class MonthRange (object):
    """
    List the first day of each month between two dates.

    >>> for day in apu.dt.MonthRange(datetime.date(2020, 2, 1), datetime.date(2020, 3, 1)):
    >>>     print(day)
    2020-02-01 (First day of Feb 2020)
    2020-03-01 (First day of March 2020)
    """
    def __init__ (self, start_date, end_date):
        assert start_date
        assert end_date

        self.start = start_date
        self.end = end_date

    def __iter__ (self):
        return MonthRangeIterator(self.start, self.end)


class MonthRangeIterator (object):

    def __init__ (self, start_date, end_date):
        self.start = datetime.date(start_date.year, start_date.month, 1)
        self.end = datetime.date(end_date.year, end_date.month, 1)
        self._current_month = self.start

    def __iter__ (self):
        return self

    def __next__ (self):
        date = self._current_month
        if date > self.end:
            raise StopIteration()
        num_month_days = calendar.monthrange(date.year, date.month)[1]
        self._current_month += datetime.timedelta(days=num_month_days)
        return date
		
    next = __next__

class WeekRange (object):
    """
    List mondays between two dates.

    >>> for day in apu.dt.WeekRange(datetime.date(2020, 2, 1), datetime.date(2020, 2, 15)):
    >>>    print(day)
    2020-01-27 (Monday of week 5)
    2020-02-03 (Monday of week 6)
    2020-02-10 (Monday of week 7)
    """
    def __init__ (self, start_date, end_date):
        self.start = start_date - datetime.timedelta(days=start_date.isocalendar()[2]-1)
        self.end = end_date + datetime.timedelta(days=7 - end_date.isocalendar()[2] - 1)

    def __getitem__ (self, index):
        if index == 0:
            return self.start
        elif index == 1:
            return self.end
        raise IndexError()

    def __iter__ (self):
        return WeekRangeIterator(self.start, self.end)

    def __str__ (self):
        return u"[{};{}]".format(str(self.start), str(self.end))

    def len (self):
        return (self.end - self.start).days / 7


class WeekRangeIterator (object):
    def __init__ (self, start_date, end_date):
        self.start = get_week_start(start_date)
        self.end = get_week_end(end_date)
        self.current_week = self.start

    def __iter__ (self):
        return self

    def __next__ (self):
        date = self.current_week
        if date > self.end:
            raise StopIteration()
        self.current_week += datetime.timedelta(days=7)
        return date

    next = __next__

	
class YearRange (object):
    def __init__ (self, start_date, end_date):
        assert start_date
        assert end_date

        self.start = start_date
        self.end = end_date

    def __iter__ (self):
        return YearRangeIterator(self.start, self.end)


class YearRangeIterator (object):

    def __init__ (self, start_date, end_date):
        self.start = datetime.date(start_date.year, 1, 1)
        self.end = datetime.date(end_date.year, 1, 1)
        self._current_year = self.start

    def __iter__ (self):
        return self

    def __next__ (self):
        date = self._current_year
        if date > self.end:
            raise StopIteration()
        num_days_in_year = (datetime.date(date.year + 1, date.month, 1) - date).days
        self._current_year += datetime.timedelta(days=num_days_in_year)
        return date

    next = __next__

def count_working_days (period_start, period_end):
    """
    Count the number of work days between two dates (count all days except Saturdays and Sundays).

    >>> apu.dt.count_working_days(datetime.date(2020, 2, 3), datetime.date(2020, 2, 9))
    5
    """
    nb_days = 0
    for x in range((period_end - period_start).days + 1):
        current_date = period_start + datetime.timedelta(days=x)
        if current_date.weekday() < 5:
            nb_days += 1
        
    return nb_days

def get_day_hour_start (now_time=None):
    """
    Get midnight of the given date.

    >>> apu.dt.get_day_hour_start(datetime.date(2020, 2, 3))
    2020-02-03 00:00:00
    """
    if not now_time:
        now_time = datetime.datetime.now()
    
    return datetime.datetime(now_time.year, now_time.month, now_time.day, 0, 0, 0)
    
def get_hour_start (now_time=None):
    """
    Get the begining of the given hour (0 minutes, 0 seconds).

    >>> apu.dt.get_hour_start(datetime.datetime(2020, 2, 1, 14, 30, 30))
    2020-02-01 14:00:00
    """
    if not now_time:
        now_time = datetime.datetime.now()
    
    return datetime.datetime(now_time.year, now_time.month, now_time.day, now_time.hour, 0, 0)

def get_hour_end (now_time=None):
    """
    Get one microsecond before the end of the given hour.

    >>> apu.dt.get_hour_end(datetime.datetime(2020, 2, 1, 14, 30, 30))
    2020-02-01 14:59:59.999999
    """
    if not now_time:
        now_time = datetime.datetime.now()
        
    hour_start = get_hour_start(now_time)
    hour_start += datetime.timedelta(hours=1)
    hour_start -= datetime.timedelta(microseconds=1)
    return hour_start
    
def get_start_of_day (dat=None):
    """
    Return the first second (midnight) of the given day.

    >>> apu.dt.get_start_of_day(datetime.date(2020, 2, 26))
    2020-02-26 00:00:00
    """
    if not dat:
        dat = datetime.datetime.today()
    return datetime.datetime(dat.year, dat.month, dat.day, 0, 0, 0)

def get_end_of_day (dat=None):
    """
    Return the last second of the given day.

    >>> apu.dt.get_end_of_day(datetime.date(2020, 2, 26))
    2020-02-26 23:59:59
    """
    if not dat:
        dat = datetime.datetime.today()
    return datetime.datetime(dat.year, dat.month, dat.day, 23, 59, 59)

def get_year_start (today=None):
    """
    Return the 1st of January of the year of the given date.
    
    >>> apu.dt.get_year_end(datetime.date(2020, 3, 1))
    2020-12-01
    """
    if today is None:
        today = datetime.date.today()
    return datetime.date(today.year, 1, 1)

def get_year_end (today=None):
    """
    Return the 31th of December of the year of the given date.

    >>> apu.dt.get_year_end(datetime.date(2020, 3, 1))
    2020-12-31
    """
    if today is None:
        today = datetime.date.today()
    return datetime.date(today.year, 12, 31)

def get_month_start (today=None, month_delta=0):
    """
    Return the first day of the month of the given date.

    >>> apu.dt.get_month_start(datetime.date(2020, 2, 10))
    2020-02-01
    """
    if today is None:
        today = datetime.date.today()

    sign = 1
    if month_delta < 0:
        sign = -1
        month_delta = -1 * month_delta

    cur_date = datetime.date(today.year, today.month, 1)

    for i in range(0, month_delta):
        cur_date = cur_date - datetime.timedelta(days=1)
        cur_date = cur_date + datetime.timedelta(days=sign * calendar.monthrange(cur_date.year, cur_date.month)[1] + 1)
    return cur_date

def get_month_end (today=None):
    """
    Return the last day of the month of the given date.

    >>> apu.dt.get_month_end(datetime.date(2020, 2, 10))
    2020-02-29
    """

    if today is None:
        today = datetime.date.today()
    num_days = calendar.monthrange(today.year, today.month)[1]
    return datetime.date(today.year, today.month, num_days)

def get_yesterday (today=None):
    """
    Return the day before the given date.

    >>> apu.dt.get_yesterday(datetime.date(2020, 3, 1))
    2020-02-29
    """
    if today is None:
        today = datetime.date.today()
    return today - datetime.timedelta(days=1)

def get_last_month (today=None):
    """
    Return the first day of the previous month.

    >>> apu.dt.get_last_month(datetime.date(2020, 2, 26))
    2020-01-01
    """
    if today is None:
        today = datetime.date.today()
    end_of_last_month = today - datetime.timedelta(days=today.day)
    return datetime.date(end_of_last_month.year, end_of_last_month.month, 1)

def get_last_month_start (today=None):
    last_month = get_last_month(today)
    return datetime.date(last_month.year, last_month.month, 1)

def get_last_month_end (today=None):
    last_month = get_last_month(today)
    num_days = calendar.monthrange(last_month.year, last_month.month)[1]
    return datetime.date(last_month.year, last_month.month, num_days)

def get_month_year_start (today=None):
    return datetime.date(today.year, 1, 1)
    
def get_last_month_year_start (today=None):
    """
    Return the first day (Jan 1st) of the year of the previous month.

    >>> apu.dt.get_last_month_year_start(datetime.date(2020, 1, 26))
    2019-01-01
    """
    return datetime.date(get_last_month(today).year, 1, 1)

def get_last_month_year_end (today=None):
    """
    Return the last day (Dec 31st) of the year of the previous month.
    
    >>> apu.dt.get_last_month_year_end(datetime.date(2020, 1, 26))
    2019-12-31
    """
    return datetime.date(get_last_month(today).year, 12, 31)

def get_ytd_month_range (today=None):
    start = get_last_month_year_start(today)
    end = get_last_month_end(today)
    return (start, end)

def is_in_range (date, range_start, range_end):
    if isinstance(range_start, datetime.date) and isinstance(range_end, datetime.date) and isinstance(date, datetime.datetime):
        date = datetime.date(date.year, date.month, date.day)
    if date != None:
        return range_start <= date and date <= range_end
    return False

def get_week_start (today=None):
    """
    Return the Monday of the week of the given date.

    >>> apu.dt.get_week_start(datetime.date(2020, 2, 26))
    2020-02-24
    """
    if not today:
        today = datetime.date.today()
    return today - datetime.timedelta(days=today.isocalendar()[2]-1)

def get_week_end (today=None):
    """
    Return the Sunday of the week of the given date.

    >>> apu.dt.get_week_start(datetime.date(2020, 2, 26))
    2020-03-01
    """
    if not today:
        today = datetime.date.today()
    return today + datetime.timedelta(days=7-today.isocalendar()[2])
    
def get_last_week_start (today=None):
    last_week_end = get_last_week_end(today)
    return last_week_end - datetime.timedelta(days=last_week_end.isocalendar()[2]-1)

def get_last_week_end (today=None):
    if not today:
        today = datetime.date.today()
    last_week_end = today - datetime.timedelta(days=today.isocalendar()[2])
    return last_week_end

def get_week_range (today=None, start=-1, end=-2):
    period_end = get_last_week_end(today) + datetime.timedelta(days=start * 7)
    period_start = period_end + datetime.timedelta(days=end * 7 + 1)
    return period_start, period_end

def get_day_range (today=None, start=1, end=1):
    #if not today:
    #    today = datetime.date.today()

    period_end = today - datetime.timedelta(days=end)
    period_start = today - datetime.timedelta(days=start)
    return period_start, period_end
    
def strftime (date_obj, fmt, default_value=None):
    if date_obj:
        return date_obj.strftime(fmt)
    return default_value

