import csv
import logging
from StringIO import StringIO
from datetime import datetime
from decimal import Decimal
from zope.interface import implements
from zope.component.hooks import getSite
from plone.uuid.interfaces import IUUID
from plone import api as plone_api

from Products.CMFCore.utils import getToolByName

from collective.simplemanagement.interfaces import IStory
from collective.simplemanagement.interfaces import IProject
from collective.simplemanagement.api.booking import create_booking
from collective.simplemanagement.browser.widgets import book_widget
from .interfaces import IBookingImporter


logger = logging.getLogger('simplemanagement.policy')


def _decode(value):
    if isinstance(value, str):
        return value.decode('utf-8')
    return value


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

    def get_project_path(self, project_id):
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

            project = brains[0]

            if project.review_state in ('closed', 'dead'):

                raise KeyError("Project '%(title)s' (%(id)s) is %(state)s" % {
                    'title': project.Title,
                    'state': project.review_state,
                    'id': project_id
                })

            path = project.getPath()
            self.add_message(
                'Got project: %s' % path
            )
            return path

        raise KeyError("Project not found: %s" % project_id)

    def get_story(self, project_id, story_id):
        brains = self._catalog.search({
            'getId': story_id,
            'object_provides': IStory.__identifier__,
            'path': self.get_project_path(project_id)
        })
        if brains:
            if len(brains) > 1:
                self.add_message(
                    'More than one story has the same id: %s' % story_id,
                    'warning'
                )
            story = brains[0]

            if story.review_state in ('in_progress',):
                obj = story.getObject()
                self.add_message(
                    'Got story: %s' % '/'.join(obj.getPhysicalPath()),
                )
                return obj

            raise KeyError("Story '%(title)s' (%(id)s) is %(state)s" % {
                'title': story.Title,
                'state': story.review_state,
                'id': story_id
            })

        raise KeyError("Story not found: %s" % story_id)

    def process_data(self, data):
        raise NotImplementedError

    def add_bookings(self, data):
        bookings = []
        for item in data:
            story = None
            try:
                story_id = item.pop('story_id')
                project_id = item.pop('project_id')
                story = self.get_story(
                    project_id.strip(),
                    story_id.strip()
                )
            except KeyError as e:
                self.add_message(e.message, 'error')
                continue

            try:
                date_ = item['date'].strip()
                time_ = item['time'].strip()
                item['time'] = Decimal(time_)
                item['date'] = datetime.strptime(
                    date_, self.DATE_FORMAT
                ).date()
                item['references'] = [('Story', IUUID(story))]
                item['owner'] = plone_api.user.get_current().id
                booking_title = _decode(item['title'])
                item['tags'] = book_widget.extract_tags(booking_title)
                item['text'] = u'@{story} {title}'.format(
                    story=story.getId(),
                    title=booking_title
                )
                del item['title']

                obj = create_booking(**item)
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
        results = self.add_bookings(self.process_data(data))
        return results


class CsvBookingImporter(BookingImporter):

    def process_data(self, data):
        fh = StringIO(data)
        return csv.DictReader(fh)
