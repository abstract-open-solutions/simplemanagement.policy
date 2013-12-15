# -*- coding: utf-8 -*-
import json
import oerplib
from datetime import datetime
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView


class CalendarLeaves(BrowserView):

    @property
    def _settings(self):
        settings = {
            "openerp.host": None,
            "openerp.port": None,
            "openerp.user": None,
            "openerp.password": None,
            "openerp.database": None
        }
        registry = getUtility(IRegistry)
        for f in settings:
            settings[f] = registry[f]
        return settings

    def _convert_date(self, time_st):
        return datetime.fromtimestamp(int(time_st)).isoformat()

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
        settings = self._settings
        leaves = []
        oerp = oerplib.OERP(
            settings['openerp.host'],
            protocol='xmlrpc',
            port=settings['openerp.port'],
        )

        # set timeout
        oerp.config['timeout'] = 10

        oerp_user = oerp.login(
            settings['openerp.user'],
            settings['openerp.password'],
            settings['openerp.database']
        )

        filters = [
            ('state', '=', 'validate'),
            ('type', '=', 'remove'),  # filter assegnazione permessi
            ('date_from', '>=', self._convert_date(start)),
            ('date_to', '<=', self._convert_date(end))
        ]

        _ids = oerp.search('hr.holidays', filters)
        brains = oerp.browse('hr.holidays', _ids)

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
                'allDay': True  # TODO: fix all day
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
