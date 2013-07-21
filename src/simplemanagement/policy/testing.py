# -*- coding: utf-8 -*-
from decimal import Decimal
from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles


class AbstractPolicyFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # pylint: disable=W0613
        import simplemanagement.policy
        self.loadZCML(package=simplemanagement.policy)
        # required by wildcard foldercontents
        import jarn.jsi18n
        self.loadZCML(package=jarn.jsi18n)
        # required by collective.simplemanagement
        z2.installProduct(app, 'Products.Poi')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'simplemanagement.policy:default')

        # Create some content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Project', 'test-project', title=u"Test project")
        test_project = portal['test-project']
        stories = []
        for i in xrange(1, 4):
            test_project.invokeFactory('Story', 'test-story-%d' % i,
                                       title=(u"Test story %d" % i))
            stories.append(test_project['test-story-%d' % i])
            stories[-1].estimate = Decimal(10 * i)
        setRoles(portal, TEST_USER_ID, ['Member'])


BASE_FIXTURE = AbstractPolicyFixture()

INTEGRATION_TESTING = IntegrationTesting(
                                    bases=(BASE_FIXTURE, ),
                                    name="AbstractPolicyFixture:Integration")

FUNCTIONAL_TESTING = FunctionalTesting(
                                    bases=(BASE_FIXTURE, ),
                                    name="AbstractPolicyFixture:Functional")
