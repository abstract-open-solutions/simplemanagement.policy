# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

from ..testing import INTEGRATION_TESTING


class TestSetup(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = getToolByName(self.portal,
                                'portal_quickinstaller')
        self.pt = getToolByName(self.portal, 'portal_types')

    def test_dependencies(self):
        products = ['collective.portletpage',
            'collective.contentleadimage',
            # 'collective.quickupload',
            # 'collective.oembed',
            # 'collective.js.oembed',
        ]

        for el in products:
            self.assertTrue(
                self.qi.isProductInstalled(el),
                    "%s is not installed" % el)

    def test_portaltypes(self):
        types = ['Event', 'Link', 'News Item']
        for el in types:
            self.assertFalse(self.pt[el].global_allow)

    def test_defaulviews(self):
        types = [('Plone Site',
                    ("folder_summary_view",
                     "folder_listing")),
                ('Folder',
                    ("folder_summary_view",
                     "folder_listing")),
                ('Topic',
                    ("folder_summary_view",
                     "folder_listing",
                     "atct_topic_view"))]

        for _id, views in types:
            self.assertEqual(self.pt[_id].view_methods, views)

    def test_defaultwf(self):
        pw = getToolByName(self.portal, 'portal_workflow')
        self.assertEqual(pw.getDefaultChain(), ('two_states_workflow',))

    def test_portlets(self):
        right = getUtility(IPortletManager, name='plone.rightcolumn')
        assignment = getMultiAdapter((self.portal, right),
                                   IPortletAssignmentMapping)
        self.assertEqual(assignment.items(), [])

    def test_portletsAddable(self):
        not_addables = ["portlets.Calendar",
                        "portlets.Classic",
                        "portlets.News",
                        "portlets.Events",
                        "portlets.Recent",
                        "portlets.Review"]

        manager = getUtility(IPortletManager, name='plone.rightcolumn')
        for portlet in manager.getAddablePortletTypes():
            self.assertNotIn(portlet.addview, not_addables)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
