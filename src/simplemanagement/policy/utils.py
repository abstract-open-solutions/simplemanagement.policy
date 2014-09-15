def get_openerp_ordernumber(orig_order_number):
    db = order_number = None
    if isinstance(orig_order_number, basestring):
        parts = orig_order_number.split('|')
        if len(parts) == 2:
            db = parts[0]
            order_number = parts[1]
        else:
            db = 'srl'
            order_number = parts[0]

    return db, order_number


def get_openerp_database_name(db_name):
    map_ = {
        'srl': 'abstract_srl',
        'snc': 'abstract_snc'
    }
    return map_.get(db_name.lower(), map_['srl'])
