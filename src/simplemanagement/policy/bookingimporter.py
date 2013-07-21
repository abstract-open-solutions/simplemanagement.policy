import logging
from datetime import datetime
from decimal import Decimal
from zope.interface import implements
from zope.component.hooks import getSite

from Products.CMFCore.utils import getToolByName

from collective.simplemanagement.interfaces import IStory
from collective.simplemanagement.interfaces import IProject
from collective.simplemanagement.booking import create_booking
from .interfaces import IBookingImporter


logger = logging.getLogger('simplemanagement.policy')


class BookingImporter(object):
    implements(IBookingImporter)

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, context=None):
        if not context:
            context = getSite()
        self.context = context
        self.messages = []

    @property
    def _catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def add_message(self, msg, level='info'):
        self.messages.append((level, msg))
        log_method = getattr(logger, level, None)
        if log_method:
            log_method(msg)

    def get_project(self, project_id):
        """Return first project by id"""
        brains = self._catalog.search({
            'getId': project_id,
            'object_provides': IProject.__identifier__,
        })

        if brains:
            if len(brains) > 1:
                self.add_message(
                    'More than one project has the same id: %s' % project_id,
                    'warning'
                )
            obj = brains[0].getObject()
            self.add_message(
                'Got project: %s' % '/'.join(obj.getPhysicalPath()),
            )
            return obj

        raise KeyError("Project not found: %s" % project_id)

    def get_story(self, project_id, story_id):
        project = self.get_project(project_id)
        brains = self._catalog.search({
            'getId': story_id,
            'object_provides': IStory.__identifier__,
            'path': '/'.join(project.getPhysicalPath())
        })
        if brains:
            if len(brains) > 1:
                self.add_message(
                    'More than one story has the same id: %s' % story_id,
                    'warning'
                )
            obj = brains[0].getObject()
            self.add_message(
                'Got story: %s' % '/'.join(obj.getPhysicalPath()),
            )
            return obj

        raise KeyError("Story not found: %s" % story_id)

    def process_data(self, data):
        bookings = []
        for item in data:
            story = None
            try:
                story = self.get_story(
                    item.pop('project_id'), item.pop('story_id')
                )
            except KeyError as e:
                self.add_message(e.message, 'error')
                continue

            try:
                item['time'] = Decimal(item['time'])
                item['date'] = datetime.strptime(
                    item['date'], self.DATE_FORMAT
                ).date()

                obj = create_booking(story, item, reindex=True)
                bookings.append(obj)
                self.add_message(
                    'Created booking: %s' % '/'.join(
                    obj.getPhysicalPath())
                )
            except Exception as e:
                self.add_message(e.message, 'error')

        return bookings

    def __call__(self, data=[]):
        """Return a list of booking objects"""
        results = self.process_data(data)
        return results
