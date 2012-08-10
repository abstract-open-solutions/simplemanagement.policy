# -*- coding: utf-8 -*-
from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class AbstractPolicyFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # pylint: disable=W0613
        import simplemanagement.policy
        self.loadZCML(package=simplemanagement.policy)
        z2.installProduct(app, 'collective.portletpage')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'simplemanagement.policy:default')


BASE_FIXTURE = AbstractPolicyFixture()

INTEGRATION_TESTING = IntegrationTesting(
                                    bases=(BASE_FIXTURE, ),
                                    name="AbstractPolicyFixture:Integration")

FUNCTIONAL_TESTING = FunctionalTesting(
                                    bases=(BASE_FIXTURE, ),
                                    name="AbstractPolicyFixture:Functional")
