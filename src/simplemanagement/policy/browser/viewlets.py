from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.simplemanagement.viewlets import ordernumber


class OrderNumber(ordernumber.OrderNumber):

    index = ViewPageTemplateFile('templates/ordernumber.pt')

    def get_otherordernumbers(self):
        catalog = getToolByName(self.context, name="portal_catalog")
        query = {
            'portal_type': ['Story', 'Iteration'],
            'path': '/'.join(self.context.getPhysicalPath()),
            'sort_on': 'path'
        }

        return [
            {
                'title': x.Title,
                'order_number': x.order_number.upper(),
                'icon': x.getIcon,
                'ordernumber_link': self.ordernumber_link(
                    x.order_number.upper()
                )
            } for x in catalog(**query) if (
                x.order_number is not None and x.UID != self.context.UID())
        ]

    def ordernumber_link(self, order_number=None):
        if not order_number:
            order_number = self.order_number

        if order_number:
            portal = api.portal.get()
            return '{}/openerp_order_redirect/{}'.format(
                portal.absolute_url(),
                order_number
            )

    def available(self):
        return (self.order_number is not None) or self.get_otherordernumbers()
