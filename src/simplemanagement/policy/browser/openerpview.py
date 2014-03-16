from plone import api
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound
from zope.component import getUtility
from zope.i18n import translate
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from ..openerp import OpenerpConnector


@implementer(IPublishTraverse)
class OpenERPBase(BrowserView):

    order_number = None

    def publishTraverse(self, request, name):
        if not self.order_number:
            self.order_number = name
        return self


class OpenERPView(OpenERPBase):

    def _get_results(self):
        if not self.order_number:
            return

        catalog = api.portal.get_tool(name='portal_catalog')
        # order_number is stored in lowercase
        order_n = self.order_number.lower()
        return catalog.searchResults({'order_number': order_n})

    def format_results(self, brains):
        pt_tool = api.portal.get_tool('portal_types')
        wf_tool = api.portal.get_tool('portal_workflow')

        results = []
        translated_pt = {}
        translated_wf = {}
        for item in brains:
            pt = item.portal_type
            if pt not in translated_pt:
                pt_title = pt_tool.get(pt).Title()
                translated_pt[pt] = self.context.translate(pt_title)

            wf_state = wf_tool.getTitleForStateOnType(item.review_state, pt)
            if wf_state not in translated_wf:
                translated_wf[wf_state] = self.context.translate(wf_state)

            results.append({
                'title': item.Title,
                'type': translated_pt[pt],
                'url': item.getURL(),
                'state': translated_wf[wf_state]
            })

        return results

    def __call__(self):
        if not self.order_number:
            raise NotFound(self.context, '', self.request)
        brains = self._get_results()
        # If there is only a result redirect to it
        if len(brains) == 1:
            self.request.response.redirect(brains[0].getURL())
            return
        else:
            self.results = self.format_results(brains)
            return super(OpenERPView, self).__call__()


class OpenOrderRedirectView(OpenERPBase):

    def __call__(self):

        if not self.order_number:
            raise NotFound(self.context, '', self.request)

        connector = OpenerpConnector()
        user_id = connector.login()
        model = 'sale.order'
        brains = [i for i in connector.search(
            model, [('name', '=', self.order_number)]
        )]

        if not brains:
            return u"Openerp order not Found"

        _id = brains[0].id
        registry = getUtility(IRegistry)
        base_url = registry['openerp.orders_base_url']

        url = base_url.format(
            host=connector.settings['openerp.host'],
            db=connector.settings['openerp.database'],
            model=model,
            id=_id
        )
        self.request.response.redirect(url)
        return
