import itertools
import datetime
import yearmonth


DAY_OF_PERIOD = 'DAY_OF_PERIOD'

# Values returned by datetime.date.weekday()
MON = MONDAY    = 0
TUE = TUESDAY   = 1
WED = WEDNESDAY = 2
THU = THURSDAY  = 3
FRI = FRIDAY    = 4
SAT = SATURDAY  = 5
SUN = SUNDAY    = 6

FUTURE = +1
PAST   = -1


class Recurrence(object):
	
	def generate(self, first_occurrence_number=0, direction=FUTURE):
		for number in itertools.count(start=first_occurrence_number, step=(-1 if direction < 0 else +1)):
			occurrence = self.get_occurrence(number)
			yield occurrence
	
	def generate_after(self, date, before=None):
		occurrence = self.get_occurrence_after(date)
		while before is None or occurrence < before:
			yield occurrence
			occurrence = self.get_occurrence_after(occurrence)
	
	def __ne__(self, other):
		return not (self == other)


class DaysBasedRecurrence(Recurrence):
	
	def __init__(self, anchor, period):
		if not isinstance(anchor, datetime.date):
			raise ValueError('Invalid anchor instance: ' + repr(anchor))
		
		self.anchor = anchor
		self.period = period
	
	def get_occurrence(self, number):
		delta_days = number * self.period
		delta = datetime.timedelta(days=delta_days)
		return self.anchor + delta
	
	def is_occurrence(self, candidate):
		delta = candidate - self.anchor
		delta_days = delta.days
		return delta_days % self.period == 0
	
	def get_occurrence_number(self, occurrence):
		delta = occurrence - self.anchor
		delta_days = delta.days
		if delta_days % self.period == 0:
			return delta_days // self.period
		else:
			raise ValueError('The date %r is not a valid occurrence' % occurrence)
	
	def get_occurrence_after(self, date):
		delta = date - self.anchor
		delta_days = delta.days
		remainder = delta_days % self.period
		delta_days += self.period - remainder
		delta = datetime.timedelta(days=delta_days)
		occurrence = self.anchor + delta
		return occurrence
		
	def __setattr__(self, attr, value):
		if attr in ('anchor', 'period') and hasattr(self, attr):
			raise AttributeError('Attribute ' + attr + ' cannot be set')
		return super(DaysBasedRecurrence, self).__setattr__(attr, value)
	
	def __eq__(self, other):
		return (isinstance(other, DaysBasedRecurrence)
				and self.anchor == other.anchor
				and self.period == other.period
			)
	
	def __hash__(self):
		return hash(self.anchor) ^ hash(self.period) 


class MonthsBasedRecurrence(Recurrence):
	
	def __init__(self, anchor, period, ordinal, day=DAY_OF_PERIOD):
		if not isinstance(anchor, yearmonth.YearMonth):
			raise ValueError('Invalid anchor instance: ' + repr(anchor))
		
		if day not in (DAY_OF_PERIOD, SUN, MON, TUE, WED, THU, FRI, SAT):
			raise ValueError('Invalid day: ' + repr(day))
		
		self.anchor = anchor
		self.period = period
		self.ordinal = ordinal
		self.day = day
	
	def get_occurrence(self, number):
		ym = self.anchor + number * self.period
		return self._date_for_period(ym)
	
	def is_occurrence(self, candidate_occurrence):
		ym = yearmonth.YearMonth.from_date(candidate_occurrence)
		delta = ym - self.anchor
		if delta % self.period != 0:
			return False
		else:
			return self._date_for_period(ym) == candidate_occurrence
	
	def get_occurrence_number(self, occurrence):
		ym = yearmonth.YearMonth.from_date(occurrence)
		delta = ym - self.anchor
		if delta % self.period == 0 and self._date_for_period(ym) == occurrence:
			return delta // self.period
		else:
			raise ValueError('The date %r is not a valid occurrence' % occurrence)
	
	def get_occurrence_after(self, date):
		ym = yearmonth.YearMonth.from_date(date)
		delta = ym - self.anchor
		remainder = delta % self.period
		if remainder != 0:
			ym += self.period - remainder
		occurrence = self._date_for_period(ym)
		if remainder == 0 and occurrence <= date:
			ym += self.period
			occurrence = self._date_for_period(ym)
		return occurrence
	
	def _date_for_period(self, ym):
		# TODO assert period > 0
		period_lower_bound_date = ym.get_first_day()
		period_ym_upper_bound = ym + self.period - 1
		period_upper_bound_date = period_ym_upper_bound.get_last_day()
		period_ym_ceil = ym + self.period
		period_ceil_date = period_ym_ceil.get_first_day()
		if self.day == DAY_OF_PERIOD:
			if self.ordinal < 0:
				return period_upper_bound_date + datetime.timedelta(days=self.ordinal+1)
			else:
				period_delta = period_ceil_date - period_lower_bound_date
				if self.ordinal > period_delta.days:
					return period_upper_bound_date
				else:
					return period_lower_bound_date + datetime.timedelta(days=self.ordinal-1)
		else:
			if self.ordinal < 0:
				last_day_of_period = period_upper_bound_date.day
				last_day_of_week = period_upper_bound_date.weekday()
				day_of_period = last_day_of_period  - (7 - self.day + last_day_of_week ) % 7 + 7 * (self.ordinal + 1)
				return period_lower_bound_date + datetime.timedelta(days=day_of_period-1)
			else:
				first_day_of_period = 1
				first_day_of_week = period_lower_bound_date.weekday()
				day_of_period = first_day_of_period + (7 + self.day - first_day_of_week) % 7 + 7 * (self.ordinal - 1)
				return period_lower_bound_date + datetime.timedelta(days=day_of_period-1)
	
	def __setattr__(self, attr, value):
		if attr in ('anchor', 'period', 'ordinal', 'day') and hasattr(self, attr):
			raise AttributeError('Attribute ' + attr + ' cannot be set')
		return super(MonthsBasedRecurrence, self).__setattr__(attr, value)
	
	def __eq__(self, other):
		return (isinstance(other, MonthsBasedRecurrence)
			and self.anchor == other.anchor
			and self.period == other.period
			and self.ordinal == other.ordinal
			and self.day == other.day
		)
	
	def __hash__(self):
		return hash(self.anchor) ^ hash(self.period) ^ hash(self.ordinal) ^ hash(self.day)  

