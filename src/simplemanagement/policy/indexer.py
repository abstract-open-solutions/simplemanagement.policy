from plone.indexer.decorator import indexer
from Products.CMFCore.interfaces import IContentish
from collective.simplemanagement.interfaces import IOrderNumber
from .utils import get_openerp_ordernumber


@indexer(IContentish)
def openerp_order_number(obj):
    if IOrderNumber.providedBy(obj):
        # Store index value in lowercase

        db_name, order_number = get_openerp_ordernumber(obj.order_number)
        if order_number:
            order_number = order_number.lower()
        return order_number
    raise AttributeError


@indexer(IContentish)
def openerp_order_number_db(obj):
    if IOrderNumber.providedBy(obj):
        # Store index value in lowercase
        db_name, order_number = get_openerp_ordernumber(obj.order_number)
        if db_name:
            db_name = db_name.lower()
        return db_name
    raise AttributeError
