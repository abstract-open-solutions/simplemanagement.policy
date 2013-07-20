from zope.interface import alsoProvides
from zope import schema
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.directives import form

from . import MessageFactory as _


class IGenericReportingConfig(form.Schema):

    activate_generic_reporting = schema.Bool(
        title=_(u"Activate Generic Reporting"),
        description=_(u'check this to create an iteration/story'
                      u' for generic booking'),
        default=True,
    )


alsoProvides(IGenericReportingConfig, form.IFormFieldProvider)