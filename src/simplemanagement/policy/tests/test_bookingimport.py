from itertools import groupby
from decimal import Decimal
from datetime import date
import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.simplemanagement.interfaces import IBooking
from collective.simplemanagement.interfaces import IStory
from collective.simplemanagement.interfaces import IProject

from ..testing import INTEGRATION_TESTING
from ..bookingimporter import BookingImporter


class TestBookingImport(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.project = self.portal['test-project']
        setRoles(self.portal, TEST_USER_ID, ['Employee'])
        self.uploader = BookingImporter(self.portal)

    def tearDown(self):
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def test_retrieve_project(self):
        project = self.uploader.get_project('test-project')
        self.assertTrue(IProject.providedBy(project))

        self.assertEqual(
            project,
            self.project
        )

        self.assertRaises(
            KeyError,
            self.uploader.get_project,
            'not-exists'
        )

    def test_retrieve_story(self):
        story = self.uploader.get_story('test-project', 'test-story-1')
        self.assertTrue(IStory.providedBy(story))
        self.assertEqual(
            story,
            self.project['test-story-1']
        )

        self.assertRaises(
            KeyError,
            self.uploader.get_story,
            'test-project',
            'not-exists'
        )

    def test_import_booking(self):
        bookings = [
            {
                'title': u'booking 1',
                'time': '1.5',
                'date': '2013-01-20',
                'project_id': 'test-project',
                'story_id': 'test-story-1'
            },

            {
                'title': u'booking 2',
                'time': '2.75',
                'date': '2013-01-22',
                'project_id': 'test-project',
                'story_id': 'not-exists'
            },

            {
                'title': u'booking 3',
                'time': '8.00',
                'date': '2013-01-23',
                'project_id': 'project-not-exists',
                'story_id': 'not-exists'
            },

        ]

        results = self.uploader(bookings)
        messages = self.uploader.messages

        self.assertEqual(len(results), 1)

        booking = self.project.restrictedTraverse(
            'test-story-1/booking-1', None)

        self.assertIsNotNone(booking)
        self.assertTrue(IBooking.providedBy(booking))

        booking_data = bookings[0]
        self.assertEqual(booking.date, date(2013, 01, 20))
        self.assertEqual(booking.time, Decimal("1.5"))

        self.assertIsNone(
            self.project.restrictedTraverse('not-exists/booking-2', None)
        )

        self.assertEqual(
            messages[-2],
            ('error', 'Story not found: not-exists')
        )

        self.assertEqual(
            messages[-1],
            ('error', 'Project not found: project-not-exists')
        )

    def test_import_wrong_data(self):
        bookings = [
            {
                'title': u'booking 4',
                'time': '1.5',
                'date': '13-01-20',
                'project_id': 'test-project',
                'story_id': 'test-story-1'
            },
            {
                'title': u'booking 5',
                'time': '1,5',
                'date': '2013-01-20',
                'project_id': 'test-project',
                'story_id': 'test-story-1'
            },
        ]
        results = self.uploader(bookings)
        messages = self.uploader.messages

        self.assertEqual(len(results), 0)

        self.assertEqual(
            messages[2],
            ('error', "time data '13-01-20' does not match format '%Y-%m-%d'")
        )

        self.assertEqual(
            messages[-1],
            ('error', "Invalid literal for Decimal: '1,5'")
        )
