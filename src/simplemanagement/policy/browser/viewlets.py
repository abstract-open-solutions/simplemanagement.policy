from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.simplemanagement.viewlets import ordernumber


class OrderNumber(ordernumber.OrderNumber):

    index = ViewPageTemplateFile('templates/ordernumber.pt')

    def ordernumber_link(self):
        portal = api.portal.get()
        return '{}/openerp_order_redirect/{}'.format(
            portal.absolute_url(),
            self.order_number
        )
