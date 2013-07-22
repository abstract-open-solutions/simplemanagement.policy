from Acquisition import aq_inner
from zope import schema
from zope.interface import Interface

from zope.component import getAdapter

from z3c.form import form, button, field
from z3c.form.interfaces import IFormLayer

from plone.z3cform.layout import wrap_form
from plone.z3cform.layout import FormWrapper
from plone.z3cform import z2
from plone.namedfile.field import NamedBlobFile

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ..interfaces import IBookingImporter
from .. import MessageFactory as _


class IUploadBookingForm(Interface):
    bookings = NamedBlobFile(
        title=_(u"File"),
        description=_(u"A CSV file that contains a list of booking."),
        required=True
    )

    file_type = schema.Choice(
        title=_(u'File type'),
        required=True,
        values=('csv',)
    )


class UploadBookingForm(form.Form):
    ignoreContext = True
    ignoreRequest = True
    fields = field.Fields(IUploadBookingForm)
    label = _(u'Upload Bookings')
    messages = []
    template = ViewPageTemplateFile("templates/titleless_form.pt")

    @button.buttonAndHandler(_(u'Upload'), name='upload')
    def handleUpload(self, __):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        importer = getAdapter(
            self.context, IBookingImporter, name=data['file_type']
        )

        importer(data['bookings'].data)
        self.messages = importer.messages
        self.status = _(u'Bookings successfully imported')


class UploadBooking(BrowserView):
    messages = []

    def form_contents(self):
        z2.switch_on(self, request_layer=IFormLayer)
        form = UploadBookingForm(aq_inner(self.context), self.request)
        form.update()
        self.messages = form.messages
        return form.render()
