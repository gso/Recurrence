import unittest
from datetime import date
from itertools import izip, izip_longest
from yearmonth import YearMonth
import recurrence


class TestDaysBasedRecurrence(unittest.TestCase):
	
	def setUp(self):
		self.dbr = recurrence.DaysBasedRecurrence(anchor=date(2012, 4, 7), period=3)

	def testAttributes(self):
		self.assertEquals(self.dbr.anchor, date(2012, 4, 7))
		self.assertEquals(self.dbr.period, 3)
	
	def testReadOnlyAttributes(self):
		def set_anchor():
			self.dbr.anchor = date(2012, 12, 20)
		self.assertRaises(AttributeError, set_anchor)
		
		def set_period():
			self.dbr.period = 10
		self.assertRaises(AttributeError, set_period)
		
		self.dbr.foo = 'bar'
	
	def testComparisons(self):
		# Equal
		self.assertTrue( self.dbr == recurrence.DaysBasedRecurrence(anchor=date(2012, 4, 7), period=3))
		self.assertFalse(self.dbr != recurrence.DaysBasedRecurrence(anchor=date(2012, 4, 7), period=3))
		
		# Different anchor
		self.assertFalse(self.dbr == recurrence.DaysBasedRecurrence(anchor=date(2012, 4, 6), period=3))
		self.assertTrue( self.dbr != recurrence.DaysBasedRecurrence(anchor=date(2012, 4, 6), period=3))

		# Different period
		self.assertFalse(self.dbr == recurrence.DaysBasedRecurrence(anchor=date(2012, 4, 7), period=4))
		self.assertTrue( self.dbr != recurrence.DaysBasedRecurrence(anchor=date(2012, 4, 7), period=4))
		
		# Different recurrence base
		self.assertFalse(self.dbr == recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=1))
		self.assertTrue( self.dbr != recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=1))


	def testGetOccurrence(self):
		self.assertEquals(self.dbr.get_occurrence(-9), date(2012, 3, 11))
		self.assertEquals(self.dbr.get_occurrence(-8), date(2012, 3, 14))
		self.assertEquals(self.dbr.get_occurrence(-7), date(2012, 3, 17))
		self.assertEquals(self.dbr.get_occurrence(-6), date(2012, 3, 20))
		self.assertEquals(self.dbr.get_occurrence(-5), date(2012, 3, 23))
		self.assertEquals(self.dbr.get_occurrence(-4), date(2012, 3, 26))
		self.assertEquals(self.dbr.get_occurrence(-3), date(2012, 3, 29))
		self.assertEquals(self.dbr.get_occurrence(-2), date(2012, 4,  1))
		self.assertEquals(self.dbr.get_occurrence(-1), date(2012, 4,  4))
		
		self.assertEquals(self.dbr.get_occurrence( 0), date(2012, 4,  7))
		
		self.assertEquals(self.dbr.get_occurrence( 1), date(2012, 4, 10))
		self.assertEquals(self.dbr.get_occurrence( 2), date(2012, 4, 13))
		self.assertEquals(self.dbr.get_occurrence( 3), date(2012, 4, 16))
		self.assertEquals(self.dbr.get_occurrence( 4), date(2012, 4, 19))
		self.assertEquals(self.dbr.get_occurrence( 5), date(2012, 4, 22))
		self.assertEquals(self.dbr.get_occurrence( 6), date(2012, 4, 25))
		self.assertEquals(self.dbr.get_occurrence( 7), date(2012, 4, 28))
		self.assertEquals(self.dbr.get_occurrence( 8), date(2012, 5,  1))
		self.assertEquals(self.dbr.get_occurrence( 9), date(2012, 5,  4))

	
	def testIsOccurrence(self):
		self.assertTrue( self.dbr.is_occurrence(date(2012, 3, 29)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 3, 30)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 3, 31)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4,  1)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  2)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  3)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4,  4)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  5)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  6)))
		
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4,  7)))
		
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  8)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4,  9)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4, 10)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4, 11)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4, 12)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4, 13)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4, 14)))
		self.assertFalse(self.dbr.is_occurrence(date(2012, 4, 15)))
		self.assertTrue( self.dbr.is_occurrence(date(2012, 4, 16)))

	
	def testGetOccurrenceNumber(self):
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 3, 29)), -3)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 3, 30)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 3, 31)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4,  1)), -2)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  2)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  3)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4,  4)), -1)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  5)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  6)))
		
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4,  7)),  0)
		
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  8)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4,  9)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4, 10)),  1)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4, 11)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4, 12)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4, 13)),  2)
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4, 14)))
		self.assertRaises(ValueError, lambda: self.dbr.get_occurrence_number(date(2012, 4, 15)))
		self.assertEquals(                    self.dbr.get_occurrence_number(date(2012, 4, 16)),  3)
	
	
	def testGetOccurrenceAfter(self):
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 3, 29)), date(2012, 4,  1))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 3, 30)), date(2012, 4,  1))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 3, 31)), date(2012, 4,  1))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4,  1)), date(2012, 4,  4))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4,  2)), date(2012, 4,  4))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4,  3)), date(2012, 4,  4))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4,  4)), date(2012, 4,  7))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4,  5)), date(2012, 4,  7))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4,  6)), date(2012, 4,  7))
		
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4,  7)), date(2012, 4, 10))
		
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4,  8)), date(2012, 4, 10))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4,  9)), date(2012, 4, 10))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4, 10)), date(2012, 4, 13))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4, 11)), date(2012, 4, 13))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4, 12)), date(2012, 4, 13))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4, 13)), date(2012, 4, 16))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4, 14)), date(2012, 4, 16))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4, 15)), date(2012, 4, 16))
		self.assertEquals(self.dbr.get_occurrence_after(date(2012, 4, 16)), date(2012, 4, 19))
	
	
	def testGenerateDefault(self):
		EXPECTED = [
			date(2012, 4,  7),
			date(2012, 4, 10),
			date(2012, 4, 13),
			date(2012, 4, 16),
			date(2012, 4, 19),
			date(2012, 4, 22),
			date(2012, 4, 25),
			date(2012, 4, 28),
			date(2012, 5,  1),
			date(2012, 5,  4),
		]
		for occurrence, expected in izip(self.dbr.generate(), EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstPositive(self):
		EXPECTED = [
			date(2012, 4, 16),
			date(2012, 4, 19),
			date(2012, 4, 22),
			date(2012, 4, 25),
			date(2012, 4, 28),
			date(2012, 5,  1),
			date(2012, 5,  4),
			date(2012, 5,  7),
			date(2012, 5, 10),
			date(2012, 5, 13),
		]
		generator = self.dbr.generate(first_occurrence_number=3)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstNegative(self):
		EXPECTED = [
			date(2012, 3, 29),
			date(2012, 4,  1),
			date(2012, 4,  4),
			date(2012, 4,  7),
			date(2012, 4, 10),
			date(2012, 4, 13),
			date(2012, 4, 16),
			date(2012, 4, 19),
			date(2012, 4, 22),
			date(2012, 4, 25),
		]
		generator = self.dbr.generate(first_occurrence_number=-3)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected, 'occurrence=%r, expected=%r' % (occurrence, expected))
	
	
	def testGenerateWithDirection(self):
		EXPECTED = [
			date(2012, 4, 16),
			date(2012, 4, 13),
			date(2012, 4, 10),
			date(2012, 4,  7),
			date(2012, 4,  4),
			date(2012, 4,  1),
			date(2012, 3, 29),
			date(2012, 3, 26),
			date(2012, 3, 23),
			date(2012, 3, 20),
		]
		generator = self.dbr.generate(first_occurrence_number=3, direction=recurrence.PAST)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	def testGenerateAfter(self):
		EXPECTED = [
			date(2012, 4, 16),
			date(2012, 4, 19),
			date(2012, 4, 22),
			date(2012, 4, 25),
			date(2012, 4, 28),
			date(2012, 5,  1),
			date(2012, 5,  4),
			date(2012, 5,  7),
			date(2012, 5, 10),
			date(2012, 5, 13),
		]
		generator = self.dbr.generate_after(date(2012, 4, 13))
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
		
	def testGenerateAfterBefore(self):
		EXPECTED = [
			date(2012, 4, 16),
			date(2012, 4, 19),
			date(2012, 4, 22),
			date(2012, 4, 25),
			date(2012, 4, 28),
			date(2012, 5,  1),
		]
		generator = self.dbr.generate_after(date(2012, 4, 13), before=date(2012, 5, 4))
		for occurrence, expected in izip_longest(generator, EXPECTED, fillvalue=None):
			self.assertIsNot(occurrence, None)
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)


class TestMonthsBasedRecurrence(unittest.TestCase):
	
	def setUp(self):
		self.mbr = recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=7)

	
	def testAttributes(self):
		self.assertEquals(self.mbr.anchor, date(2012, 4, 7))
		self.assertEquals(self.mbr.period, 3)
		self.assertEquals(self.mbr.ordinal, 7)
		self.assertEquals(self.mbr.day, recurrence.DAY_OF_MONTH)
	
	
	def testReadOnlyAttributes(self):
		def set_anchor():
			self.mbr.anchor = date(2012, 12, 20)
		self.assertRaises(AttributeError, set_anchor)
		
		def set_period():
			self.mbr.recurrence.period = 10
		self.assertRaises(AttributeError, set_period)
		
		def set_ordinal():
			self.mbr.recurrence.ordinal = 10
		self.assertRaises(AttributeError, set_ordinal)
		
		def set_day():
			self.mbr.recurrence.day = recurrence.MONDAY
		self.assertRaises(AttributeError, set_day)
		
		self.mbr.foo = 'bar'
	
	
	def testComparisons(self):
		# Equal
		self.assertTrue( self.mbr == recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=7))
		self.assertFalse(self.mbr != recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=7))
		
		# Different anchor
		self.assertFalse(self.mbr == recurrence.MonthsBasedRecurrence(anchor=YearMonth(2011, 4), period=3, ordinal=7))
		self.assertTrue( self.mbr != recurrence.MonthsBasedRecurrence(anchor=YearMonth(2011, 4), period=3, ordinal=7))
		
		# Different period
		self.assertFalse(self.mbr == recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=4, ordinal=7))
		self.assertTrue( self.mbr != recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=4, ordinal=7))
		
		# Different ordinal
		self.assertFalse(self.mbr == recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=8))
		self.assertTrue( self.mbr != recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=8))
		
		# Different day
		self.assertFalse(self.mbr == recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=7, day=recurrence.MONDAY))
		self.assertTrue( self.mbr != recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=7, day=recurrence.MONDAY))
		
		# Different recurrence base
		self.assertFalse(self.mbr == recurrence.DaysBasedRecurrence(anchor=date(2012, 4, 7), period=3))
		self.assertTrue( self.mbr != recurrence.DaysBasedRecurrence(anchor=date(2012, 4, 7), period=3))


class TestMonthsBasedRecurrenceWithPositiveDayOfMonth(unittest.TestCase):
	
	def setUp(self):
		self.mbr = recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=7)
		
	
	def testGetOccurrence(self):
		self.assertEquals(self.mbr.get_occurrence(-3), date(2011,  7, 7))
		self.assertEquals(self.mbr.get_occurrence(-2), date(2011, 10, 7))
		self.assertEquals(self.mbr.get_occurrence(-1), date(2012,  1, 7))
		
		self.assertEquals(self.mbr.get_occurrence( 0), date(2012,  4, 7))
		
		self.assertEquals(self.mbr.get_occurrence( 1), date(2012,  7, 7))
		self.assertEquals(self.mbr.get_occurrence( 2), date(2012, 10, 7))
		self.assertEquals(self.mbr.get_occurrence( 3), date(2013,  1, 7))
	
	
	def testIsOccurrence(self):
		self.assertTrue( self.mbr.is_occurrence(date(2011, 10,  7)))
		self.assertFalse(self.mbr.is_occurrence(date(2011, 11,  7)))
		self.assertFalse(self.mbr.is_occurrence(date(2011, 12,  7)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  1,  6)))
		self.assertTrue( self.mbr.is_occurrence(date(2012,  1,  7)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  1,  8)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  2,  7)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  3,  7)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4,  6)))
		
		self.assertTrue( self.mbr.is_occurrence(date(2012,  4,  7)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4,  8)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  5,  7)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  6,  7)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  7,  6)))
		self.assertTrue( self.mbr.is_occurrence(date(2012,  7,  7)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  7,  8)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  8,  7)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  9,  7)))
		self.assertTrue( self.mbr.is_occurrence(date(2012, 10,  7)))
	
	
	def testGetOccurrenceNumber(self):
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2011, 10,  7)), -2)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011, 11,  7)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011, 12,  7)))
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  1,  6)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  1,  7)), -1)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  1,  8)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  2,  7)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  3,  7)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4,  6)))
		
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  4,  7)),  0)
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4,  8)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  5,  7)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  6,  7)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  7,  6)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  7,  7)),  1)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  7,  8)))
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  8,  7)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  9,  7)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012, 10,  7)),  2)
	
	
	def testGetOccurrenceAfter(self):
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 10,  7)), date(2012,  1,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 11,  7)), date(2012,  1,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 12,  7)), date(2012,  1,  7))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  1,  6)), date(2012,  1,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  1,  7)), date(2012,  4,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  1,  8)), date(2012,  4,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  2,  7)), date(2012,  4,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  3,  7)), date(2012,  4,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4,  6)), date(2012,  4,  7))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4,  7)), date(2012,  7,  7))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4,  8)), date(2012,  7,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  5,  7)), date(2012,  7,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  6,  7)), date(2012,  7,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  7,  6)), date(2012,  7,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  7,  7)), date(2012, 10,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  7,  8)), date(2012, 10,  7))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  8,  7)), date(2012, 10,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  9,  7)), date(2012, 10,  7))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012, 10,  7)), date(2013,  1,  7))
	
	
	def testGenerateDefault(self):
		EXPECTED = [
			date(2012,  4,  7),
			date(2012,  7,  7),
			date(2012, 10,  7),
			date(2013,  1,  7),
			date(2013,  4,  7),
			date(2013,  7,  7),
			date(2013, 10,  7),
			date(2014,  1,  7),
			date(2014,  4,  7),
			date(2014,  7,  7),
		]
		for occurrence, expected in izip(self.mbr.generate(), EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstPositive(self):
		EXPECTED = [
			date(2013,  1,  7),
			date(2013,  4,  7),
			date(2013,  7,  7),
			date(2013, 10,  7),
			date(2014,  1,  7),
			date(2014,  4,  7),
			date(2014,  7,  7),
			date(2014, 10,  7),
			date(2015,  1,  7),
			date(2015,  4,  7),
		]
		generator = self.mbr.generate(first_occurrence_number=3)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstNegative(self):
		EXPECTED = [
			date(2011,  7,  7),
			date(2011, 10,  7),
			date(2012,  1,  7),
			date(2012,  4,  7),
			date(2012,  7,  7),
			date(2012, 10,  7),
			date(2013,  1,  7),
			date(2013,  4,  7),
			date(2013,  7,  7),
			date(2013, 10,  7),
		]
		for occurrence, expected in izip(self.mbr.generate(first_occurrence_number=-3), EXPECTED):
			self.assertEquals(occurrence, expected, 'occurrence=%r, expected=%r' % (occurrence, expected))
	
	
	def testGenerateWithDirection(self):
		EXPECTED = [
			date(2013,  1,  7),
			date(2012, 10,  7),
			date(2012,  7,  7),
			date(2012,  4,  7),
			date(2012,  1,  7),
			date(2011, 10,  7),
			date(2011,  7,  7),
			date(2011,  4,  7),
			date(2011,  1,  7),
			date(2010, 10,  7),
		]
		generator = self.mbr.generate(
				first_occurrence_number=3,
				direction=recurrence.PAST
			)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	def testGenerateAfter(self):
		EXPECTED = [
			date(2013,  1,  7),
			date(2013,  4,  7),
			date(2013,  7,  7),
			date(2013, 10,  7),
			date(2014,  1,  7),
			date(2014,  4,  7),
			date(2014,  7,  7),
			date(2014, 10,  7),
			date(2015,  1,  7),
			date(2015,  4,  7),
		]
		generator = self.mbr.generate_after(date(2012, 10, 7))
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
		
	def testGenerateAfterBefore(self):
		EXPECTED = [
			date(2013,  1,  7),
			date(2013,  4,  7),
			date(2013,  7,  7),
			date(2013, 10,  7),
			date(2014,  1,  7),
			date(2014,  4,  7),
			date(2014,  7,  7),
		]
		generator = self.mbr.generate_after(date(2012, 10, 7), before=date(2014, 10, 7))
		for occurrence, expected in izip_longest(generator, EXPECTED, fillvalue=None):
			self.assertIsNot(occurrence, None)
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)


class TestMonthsBasedRecurrenceWithNegativeDayOfMonth(unittest.TestCase):
	def setUp(self):
		self.mbr = recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=3, ordinal=-7)
		
	
	def testGetOccurrence(self):
		self.assertEquals(self.mbr.get_occurrence(-3), date(2011,  7, 25))
		self.assertEquals(self.mbr.get_occurrence(-2), date(2011, 10, 25))
		self.assertEquals(self.mbr.get_occurrence(-1), date(2012,  1, 25))
		
		self.assertEquals(self.mbr.get_occurrence( 0), date(2012,  4, 24))
		
		self.assertEquals(self.mbr.get_occurrence( 1), date(2012,  7, 25))
		self.assertEquals(self.mbr.get_occurrence( 2), date(2012, 10, 25))
		self.assertEquals(self.mbr.get_occurrence( 3), date(2013,  1, 25))
	
	
	def testIsOccurrence(self):
		self.assertTrue( self.mbr.is_occurrence(date(2011, 10, 25)))
		self.assertFalse(self.mbr.is_occurrence(date(2011, 11, 24)))
		self.assertFalse(self.mbr.is_occurrence(date(2011, 12, 25)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  1, 24)))
		self.assertTrue( self.mbr.is_occurrence(date(2012,  1, 25)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  1, 26)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  2, 23)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  3, 25)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 23)))
		
		self.assertTrue( self.mbr.is_occurrence(date(2012,  4, 24)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 25)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  5, 25)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  6, 24)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  7, 24)))
		self.assertTrue( self.mbr.is_occurrence(date(2012,  7, 25)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  7, 26)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  8, 25)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  9, 24)))
		self.assertTrue( self.mbr.is_occurrence(date(2012, 10, 25)))
	
	
	def testGetOccurrenceNumber(self):
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2011, 10, 25)), -2)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011, 11, 24)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011, 12, 25)))
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  1, 24)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  1, 25)), -1)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  1, 26)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  2, 23)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  3, 25)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 23)))
		
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  4, 24)),  0)
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 25)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  5, 25)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  6, 24)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  7, 24)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  7, 25)),  1)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  7, 26)))
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  8, 25)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  9, 24)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012, 10, 25)),  2)
	
	
	def testGetOccurrenceAfter(self):
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 10, 25)), date(2012,  1, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 11, 24)), date(2012,  1, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 12, 25)), date(2012,  1, 25))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  1, 24)), date(2012,  1, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  1, 25)), date(2012,  4, 24))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  1, 26)), date(2012,  4, 24))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  2, 23)), date(2012,  4, 24))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  3, 25)), date(2012,  4, 24))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 24)), date(2012,  7, 25))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 25)), date(2012,  7, 25))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 26)), date(2012,  7, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  5, 25)), date(2012,  7, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  6, 24)), date(2012,  7, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  7, 24)), date(2012,  7, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  7, 25)), date(2012, 10, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  7, 26)), date(2012, 10, 25))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  8, 25)), date(2012, 10, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  9, 24)), date(2012, 10, 25))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012, 10, 25)), date(2013,  1, 25))
	
	
	def testGenerateDefault(self):
		EXPECTED = [
			date(2012,  4, 24),
			date(2012,  7, 25),
			date(2012, 10, 25),
			date(2013,  1, 25),
			date(2013,  4, 24),
			date(2013,  7, 25),
			date(2013, 10, 25),
			date(2014,  1, 25),
			date(2014,  4, 24),
			date(2014,  7, 25),
		]
		for occurrence, expected in izip(self.mbr.generate(), EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstPositive(self):
		EXPECTED = [
			date(2013,  1, 25),
			date(2013,  4, 24),
			date(2013,  7, 25),
			date(2013, 10, 25),
			date(2014,  1, 25),
			date(2014,  4, 24),
			date(2014,  7, 25),
			date(2014, 10, 25),
			date(2015,  1, 25),
			date(2015,  4, 24),
		]
		generator = self.mbr.generate(first_occurrence_number=3)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstNegative(self):
		EXPECTED = [
			date(2011,  7, 25),
			date(2011, 10, 25),
			date(2012,  1, 25),
			date(2012,  4, 24),
			date(2012,  7, 25),
			date(2012, 10, 25),
			date(2013,  1, 25),
			date(2013,  4, 24),
			date(2013,  7, 25),
			date(2013, 10, 25),
		]
		generator = self.mbr.generate(first_occurrence_number=-3)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected, 'occurrence=%r, expected=%r' % (occurrence, expected))
	
	
	def testGenerateWithDirection(self):
		EXPECTED = [
			date(2013,  1, 25),
			date(2012, 10, 25),
			date(2012,  7, 25),
			date(2012,  4, 24),
			date(2012,  1, 25),
			date(2011, 10, 25),
			date(2011,  7, 25),
			date(2011,  4, 24),
			date(2011,  1, 25),
			date(2010, 10, 25),
		]
		generator = self.mbr.generate(first_occurrence_number=3, direction=recurrence.PAST)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	def testGenerateAfter(self):
		EXPECTED = [
			date(2013,  1, 25),
			date(2013,  4, 24),
			date(2013,  7, 25),
			date(2013, 10, 25),
			date(2014,  1, 25),
			date(2014,  4, 24),
			date(2014,  7, 25),
			date(2014, 10, 25),
			date(2015,  1, 25),
			date(2015,  4, 24),
		]
		generator = self.mbr.generate_after(date(2012, 10, 25))
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
		
	def testGenerateAfterBefore(self):
		EXPECTED = [
			date(2013,  1, 25),
			date(2013,  4, 24),
			date(2013,  7, 25),
			date(2013, 10, 25),
			date(2014,  1, 25),
			date(2014,  4, 24),
			date(2014,  7, 25),
		]
		generator = self.mbr.generate_after(date(2012, 10, 25), before=date(2014, 10, 25))
		for occurrence, expected in izip_longest(generator, EXPECTED, fillvalue=None):
			self.assertIsNot(occurrence, None)
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)


class TestMonthsBasedRecurrenceWithPositiveDayOfWeek(unittest.TestCase):
	
	def setUp(self):
		self.mbr = recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=4, ordinal=3, day=recurrence.TUESDAY)

	
	def testGetOccurrence(self):
		self.assertEquals(self.mbr.get_occurrence(-3), date(2011,  4, 19))
		self.assertEquals(self.mbr.get_occurrence(-2), date(2011,  8, 16))
		self.assertEquals(self.mbr.get_occurrence(-1), date(2011, 12, 20))
		
		self.assertEquals(self.mbr.get_occurrence( 0), date(2012,  4, 17))
		
		self.assertEquals(self.mbr.get_occurrence( 1), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence( 2), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence( 3), date(2013,  4, 16))
	
	
	def testIsOccurrence(self):
		self.assertTrue( self.mbr.is_occurrence(date(2011,  8, 16)))
		self.assertFalse(self.mbr.is_occurrence(date(2011,  9, 20)))
		self.assertFalse(self.mbr.is_occurrence(date(2011, 10, 18)))
		self.assertFalse(self.mbr.is_occurrence(date(2011, 11, 15)))
		self.assertTrue( self.mbr.is_occurrence(date(2011, 12, 20)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  1, 17)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  2, 21)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  3, 20)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 10)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 16)))
		self.assertTrue( self.mbr.is_occurrence(date(2012,  4, 17)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 18)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 24)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  5, 15)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  6, 19)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  7, 17)))
		self.assertTrue( self.mbr.is_occurrence(date(2012,  8, 21)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  9, 18)))
		self.assertFalse(self.mbr.is_occurrence(date(2012, 10, 16)))
		self.assertFalse(self.mbr.is_occurrence(date(2012, 11, 20)))
		self.assertTrue( self.mbr.is_occurrence(date(2012, 12, 18)))
	
	
	def testGetOccurrenceNumber(self):
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2011,  8, 16)), -2)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011,  9, 20)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011, 10, 18)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011, 11, 15)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2011, 12, 20)), -1)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  1, 17)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  2, 21)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  3, 20)))
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 10)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 16)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  4, 17)),  0)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 18)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 24)))
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  5, 15)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  6, 19)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  7, 17)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  8, 21)),  1)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  9, 18)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012, 10, 16)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012, 11, 20)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012, 12, 18)),  2)
	
	
	def testGetOccurrenceAfter(self):
		self.assertEquals(self.mbr.get_occurrence_after(date(2011,  8, 16)), date(2011, 12, 20))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011,  9, 20)), date(2011, 12, 20))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 10, 18)), date(2011, 12, 20))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 11, 15)), date(2011, 12, 20))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 12, 20)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  1, 17)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  2, 21)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  3, 20)), date(2012,  4, 17))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 10)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 16)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 17)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 18)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 24)), date(2012,  8, 21))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  5, 15)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  6, 19)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  7, 17)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  8, 21)), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  9, 18)), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012, 10, 16)), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012, 11, 20)), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012, 12, 18)), date(2013,  4, 16))
	
	
	def testGenerateDefault(self):
		EXPECTED = [
			date(2012,  4, 17),
			date(2012,  8, 21),
			date(2012, 12, 18),
			date(2013,  4, 16),
			date(2013,  8, 20),
			date(2013, 12, 17),
			date(2014,  4, 15),
			date(2014,  8, 19),
			date(2014, 12, 16),
			date(2015,  4, 21),
		]
		for occurrence, expected in izip(self.mbr.generate(), EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstPositive(self):
		EXPECTED = [
			date(2013,  4, 16),
			date(2013,  8, 20),
			date(2013, 12, 17),
			date(2014,  4, 15),
			date(2014,  8, 19),
			date(2014, 12, 16),
			date(2015,  4, 21),
			date(2015,  8, 18),
			date(2015, 12, 15),
			date(2016,  4, 19),
		]
		generator = self.mbr.generate(first_occurrence_number=3)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstNegative(self):
		EXPECTED = [
			date(2011,  4, 19),
			date(2011,  8, 16),
			date(2011, 12, 20),
			date(2012,  4, 17),
			date(2012,  8, 21),
			date(2012, 12, 18),
			date(2013,  4, 16),
			date(2013,  8, 20),
			date(2013, 12, 17),
			date(2014,  4, 15),
		]
		generator = self.mbr.generate(first_occurrence_number=-3)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected, 'occurrence=%r, expected=%r' % (occurrence, expected))
	
	
	def testGenerateWithDirection(self):
		EXPECTED = [
			date(2013,  4, 16),
			date(2012, 12, 18),
			date(2012,  8, 21),
			date(2012,  4, 17),
			date(2011, 12, 20),
			date(2011,  8, 16),
			date(2011,  4, 19),
			date(2010, 12, 21),
			date(2010,  8, 17),
			date(2010,  4, 20),
		]
		generator = self.mbr.generate(first_occurrence_number=3, direction=recurrence.PAST)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	def testGenerateAfter(self):
		EXPECTED = [
			date(2013,  4, 16),
			date(2013,  8, 20),
			date(2013, 12, 17),
			date(2014,  4, 15),
			date(2014,  8, 19),
			date(2014, 12, 16),
			date(2015,  4, 21),
			date(2015,  8, 18),
			date(2015, 12, 15),
			date(2016,  4, 19),
		]
		generator = self.mbr.generate_after(date(2012, 12, 18))
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
		
	def testGenerateAfterBefore(self):
		EXPECTED = [
			date(2013,  4, 16),
			date(2013,  8, 20),
			date(2013, 12, 17),
			date(2014,  4, 15),
			date(2014,  8, 19),
			date(2014, 12, 16),
			date(2015,  4, 21),
		]
		generator = self.mbr.generate_after(date(2012, 12, 18), before=date(2015, 8, 18))
		for occurrence, expected in izip_longest(generator, EXPECTED, fillvalue=None):
			self.assertIsNot(occurrence, None)
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)


class TestMonthsBasedRecurrenceWithNegativeDayOfWeek(unittest.TestCase):
	def setUp(self):
		self.mbr = recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 4), period=4, ordinal=-2, day=recurrence.TUESDAY)

	
	def testGetOccurrence(self):
		self.assertEquals(self.mbr.get_occurrence(-3), date(2011,  4, 19))
		self.assertEquals(self.mbr.get_occurrence(-2), date(2011,  8, 23))
		self.assertEquals(self.mbr.get_occurrence(-1), date(2011, 12, 20))
		
		self.assertEquals(self.mbr.get_occurrence( 0), date(2012,  4, 17))
		
		self.assertEquals(self.mbr.get_occurrence( 1), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence( 2), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence( 3), date(2013,  4, 23))
	
	
	def testIsOccurrence(self):
		self.assertTrue( self.mbr.is_occurrence(date(2011,  8, 23)))
		self.assertFalse(self.mbr.is_occurrence(date(2011,  9, 20)))
		self.assertFalse(self.mbr.is_occurrence(date(2011, 10, 18)))
		self.assertFalse(self.mbr.is_occurrence(date(2011, 11, 22)))
		self.assertTrue( self.mbr.is_occurrence(date(2011, 12, 20)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  1, 24)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  2, 21)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  3, 20)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 10)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 16)))
		self.assertTrue( self.mbr.is_occurrence(date(2012,  4, 17)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 18)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  4, 24)))
		
		self.assertFalse(self.mbr.is_occurrence(date(2012,  5, 22)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  6, 19)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  7, 24)))
		self.assertTrue( self.mbr.is_occurrence(date(2012,  8, 21)))
		self.assertFalse(self.mbr.is_occurrence(date(2012,  9, 18)))
		self.assertFalse(self.mbr.is_occurrence(date(2012, 10, 23)))
		self.assertFalse(self.mbr.is_occurrence(date(2012, 11, 20)))
		self.assertTrue( self.mbr.is_occurrence(date(2012, 12, 18)))
	
	
	def testGetOccurrenceNumber(self):
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2011,  8, 23)), -2)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011,  9, 20)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011, 10, 18)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2011, 11, 22)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2011, 12, 20)), -1)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  1, 24)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  2, 21)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  3, 20)))
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 10)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 16)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  4, 17)),  0)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 18)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  4, 24)))
		
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  5, 22)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  6, 19)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  7, 24)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012,  8, 21)),  1)
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012,  9, 18)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012, 10, 23)))
		self.assertRaises(ValueError, lambda: self.mbr.get_occurrence_number(date(2012, 11, 20)))
		self.assertEquals(                    self.mbr.get_occurrence_number(date(2012, 12, 18)),  2)
	
	
	def testGetOccurrenceAfter(self):
		self.assertEquals(self.mbr.get_occurrence_after(date(2011,  8, 23)), date(2011, 12, 20))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011,  9, 20)), date(2011, 12, 20))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 10, 18)), date(2011, 12, 20))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 11, 22)), date(2011, 12, 20))
		self.assertEquals(self.mbr.get_occurrence_after(date(2011, 12, 20)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  1, 24)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  2, 21)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  3, 20)), date(2012,  4, 17))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 10)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 16)), date(2012,  4, 17))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 17)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 18)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  4, 24)), date(2012,  8, 21))
		
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  5, 22)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  6, 19)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  7, 24)), date(2012,  8, 21))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  8, 21)), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012,  9, 18)), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012, 10, 23)), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012, 11, 20)), date(2012, 12, 18))
		self.assertEquals(self.mbr.get_occurrence_after(date(2012, 12, 18)), date(2013,  4, 23))
	
	
	def testGenerateDefault(self):
		EXPECTED = [
			date(2012,  4, 17),
			date(2012,  8, 21),
			date(2012, 12, 18),
			date(2013,  4, 23),
			date(2013,  8, 20),
			date(2013, 12, 24),
			date(2014,  4, 22),
			date(2014,  8, 19),
			date(2014, 12, 23),
			date(2015,  4, 21),
		]
		for occurrence, expected in izip(self.mbr.generate(), EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstPositive(self):
		EXPECTED = [
			date(2013,  4, 23),
			date(2013,  8, 20),
			date(2013, 12, 24),
			date(2014,  4, 22),
			date(2014,  8, 19),
			date(2014, 12, 23),
			date(2015,  4, 21),
			date(2015,  8, 18),
			date(2015, 12, 22),
			date(2016,  4, 19),
		]
		generator = self.mbr.generate(first_occurrence_number=3)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	
	def testGenerateWithFirstNegative(self):
		EXPECTED = [
			date(2011,  4, 19),
			date(2011,  8, 23),
			date(2011, 12, 20),
			date(2012,  4, 17),
			date(2012,  8, 21),
			date(2012, 12, 18),
			date(2013,  4, 23),
			date(2013,  8, 20),
			date(2013, 12, 24),
			date(2014,  4, 22),
		]
		generator = self.mbr.generate(first_occurrence_number=-3)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected, 'occurrence=%r, expected=%r' % (occurrence, expected))
	
	
	def testGenerateWithDirection(self):
		EXPECTED = [
			date(2013,  4, 23),
			date(2012, 12, 18),
			date(2012,  8, 21),
			date(2012,  4, 17),
			date(2011, 12, 20),
			date(2011,  8, 23),
			date(2011,  4, 19),
			date(2010, 12, 21),
			date(2010,  8, 24),
			date(2010,  4, 20),
		]
		generator = self.mbr.generate(first_occurrence_number=3, direction=recurrence.PAST)
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
	
	def testGenerateAfter(self):
		EXPECTED = [
			date(2013,  4, 23),
			date(2013,  8, 20),
			date(2013, 12, 24),
			date(2014,  4, 22),
			date(2014,  8, 19),
			date(2014, 12, 23),
			date(2015,  4, 21),
			date(2015,  8, 18),
			date(2015, 12, 22),
			date(2016,  4, 19),
		]
		generator = self.mbr.generate_after(date(2012, 12, 18))
		for occurrence, expected in izip(generator, EXPECTED):
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)
		
	def testGenerateAfterBefore(self):
		EXPECTED = [
			date(2013,  4, 23),
			date(2013,  8, 20),
			date(2013, 12, 24),
			date(2014,  4, 22),
			date(2014,  8, 19),
			date(2014, 12, 23),
			date(2015,  4, 21),
		]
		generator = self.mbr.generate_after(date(2012, 12, 18), before=date(2015, 8, 18))
		for occurrence, expected in izip_longest(generator, EXPECTED, fillvalue=None):
			self.assertIsNot(occurrence, None)
			self.assertEquals(occurrence, expected,
					'occurrence=%r, expected=%r' % (occurrence, expected)
				)



if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()