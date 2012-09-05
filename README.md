
FORK of [erdavila / Recurrence](https://github.com/erdavila/Recurrence):

- fixes bug in `def _date_for_yearmonth(self, ym):` method (ref. [issue #2]( https://github.com/erdavila/Recurrence/issues/2))
- adds a year recurrence capability (ref. [issue #1]( https://github.com/erdavila/Recurrence/issues/1)) - a month based recur object can now recur on any day in a recur period.

The algorithm does not as yet accommodate, e.g., the first Monday in the first full week of the month (but could be implemented relatively easily I would think).  It would also at some point need a way to add more complex include/ exclude type date recur rules.

Other similar libraries:

- [python-dateutil](http://labix.org/python-dateutil), which implements rrule
- [jkbr / rrule](https://github.com/jkbr/rrule), a standalone Javascript port of python-dateutil
- [node-date-recur](https://github.com/appsattic/node-date-recur) node plugin

erdavila's approach even though not complete does have its strengths in terms of the algorithm used as a starting point.
