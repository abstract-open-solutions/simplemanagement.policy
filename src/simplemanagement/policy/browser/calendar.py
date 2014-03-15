# -*- coding: utf-8 -*-
import json

from datetime import datetime
from time import time
from plone.memoize import ram
from Products.Five.browser import BrowserView
from ..openerp import OpenerpConnector


class CalendarLeaves(BrowserView):

    def _convert_date(self, time_st):
        return datetime.fromtimestamp(int(time_st)).isoformat()

    @ram.cache(lambda *args: time() // (60 * 60))
    def _results(self, start, end):
        """[
              {
                "title": "All day Event 2 ago",
                "description": "...",
                "start": "2013-08-02",
                "allDay": true
              },
              {
                "title": "One hour Event - 20 ago 10-11",
                "description": "...",
                "start": "2013-08-20 10:00",
                "end": "2013-08-20 11:00",
                "allDay": false
              },
              {
                "title": "Eight days Event 23 ago",
                "description": "...",
                "start": "2013-08-23",
                "end": "2013-08-30",
                "allDay": true
              }
            ]

        """

        leaves = []
        filters = [
            ('state', '=', 'validate'),
            ('type', '=', 'remove'),  # filter assegnazione permessi
            ('date_from', '>=', self._convert_date(start)),
            ('date_to', '<=', self._convert_date(end))
        ]

        connector = OpenerpConnector()
        user_id = connector.login()
        brains = connector.search('hr.holidays', filters)

        for item in brains:
            employee_name = item.employee_id.name
            title = u"[{0}] - {1}".format(
                ''.join([i[0] for i in employee_name.split(' ')]),
                item.holiday_status_id.name
            )
            description = u"{0}, {1}".format(
                employee_name,
                item.name
            )

            data = {
                'id': item.id,
                'title': title,
                'description': description,
                'start': item.date_from.isoformat(),
                'end': item.date_to.isoformat(),
                'allDay': item.entire_day_flag
                # 'number_of_days': holiday.number_of_days_temp,
                # 'number_of_hours': holiday.number_of_hours
            }
            leaves.append(data)

        return leaves

    def __call__(self):
        start = self.request.get('start')
        end = self.request.get('end')
        if not (start and end) or not (start.isdigit() and start.isdigit()):
            raise ValueError("Start and end dates are required")

        results = self._results(start, end)
        self.request.response.setHeader("Content-type", "application/json")
        return json.dumps(results)
