from plone import api
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView


@implementer(IPublishTraverse)
class OpenERPView(BrowserView):

    order_number = None

    def publishTraverse(self, request, name):
        if not self.order_number:
            self.order_number = name
        return self

    def results(self):
        if not self.order_number:
            return

        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog.searchResults({'order_number': self.order_number})
        results = []
        for item in brains:
            results.append({
                'title': item.Title,
                'type': item.portal_type,
                'url': item.getURL()
            })
        return results

    def __call__(self):
        if not self.order_number:
            raise NotFound(self.context, '', self.request)
        return super(OpenERPView, self).__call__()
