
FORK of https://github.com/erdavila/Recurrence

- fixes bug in 'def _date_for_yearmonth(self, ym):' method (ref. [issue #2]( https://github.com/erdavila/Recurrence/issues/2))
- adds a year recurrence capability (ref. [issue #1]( https://github.com/erdavila/Recurrence/issues/1)) - a month based recur object can now recur on any day in a recur period.

The algorithm does not accommodate, e.g., the first Monday in the first full week of the month (but could be implemented relatively easily).

There already exists a fully implemented standalone recur rule library by the name of [python-dateutil](http://labix.org/python-dateutil) which implements rrule.  In terms of the development of web apps, there as a standalone Javascript port of [python-dateutil](https://github.com/jkbr/rrule), serverside there is also the [node-date-recur](https://github.com/appsattic/node-date-recur) node plugin.   erdavila's approach though does have its strengths in terms of the algorithm.