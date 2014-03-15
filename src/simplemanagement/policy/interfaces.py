from zope.interface import alsoProvides
from zope.interface import Interface
from zope import schema
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.autoform import directives as form

from collective.simplemanagement.interfaces import IBrowserLayer as IBaseLayer

from . import MessageFactory as _


class IBrowserLayer(IBaseLayer):
    """The browser layer of the package"""


class IGenericReportingConfig(model.Schema):

    activate_generic_reporting = schema.Bool(
        title=_(u"Activate Generic Reporting"),
        description=_(u'check this to create an iteration/story'
                      u' for generic booking'),
        default=True,
    )


alsoProvides(IGenericReportingConfig, IFormFieldProvider)


class IBookingImporter(Interface):
    """Utility to import booking ct from a list of dictionaries
    """

    def add_message(msg, level='info'):
        """Add message in self.message property and in standard log
        """

    def get_project_path(project_id):
        """Look into portal_catalog and return first project with project_id
        """
    def get_story(project_id, story_id):
        """Look into portal_catalog and return first story found
        """

    def process_data(data):
        """Process booking data and create booking into specific story"""

    def __call__(data=[]):
        """Method to create a list of booking content type
        using a list as source

        A row in events should be a dictionary with fields
        * title
        * project_id
        * story_id
        * date
        * time

        It returns a list of bookings
        """
