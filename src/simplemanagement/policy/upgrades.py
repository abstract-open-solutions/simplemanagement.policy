import logging
from datetime import datetime
from datetime import date
from Products.CMFPlone.utils import getToolByName

# pylint: disable=W0613


LOGGER = 'simplemanagement.policy'
DEFAULT_PROFILE = 'profile-simplemanagement.policy:default'


def getLogger(logger=None):
    if logger is None:
        logger = logging.getLogger(LOGGER)
    return logger


def upgrade_to_1001(context, logger=None):
    logger = getLogger(logger)
    logger.info("Fixing portal_javascripts")
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'jsregistry')


def upgrade_to_1002(context, logger=None):
    logger = getLogger(logger)
    logger.info("Import browserlayer")
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'browserlayer')
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'cssregistry')


def upgrade_to_1003(context, logger=None):
    logger = getLogger(logger)
    logger.info("update registry")
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'plone.app.registry')


def upgrade_to_1004(context, logger=None):
    logger = getLogger(logger)
    logger.info("fix compass")

    tool = getToolByName(context, 'portal_compass')
    months = {
        'Gennaio': '01',
        'januar': '01',
        'Febbraio': '02',
        'februar': '02',
        'Marzo': '03',
        'Aprile': '04',
        'Maggio': '05',
        'Giugno': '06',
        'Luglio': '07',
        'Agosto': '08',
        'Settembre': '09',
        'Ottobre': '10',
        'Novembre': '11',
        'november': '11',
        'desember': '12',
        'Dicembre': '12'
    }

    to_convert = [
        'plan_end',
        'plan_start'
    ]

    def convert_date(date_str):
        for m in months.keys():
            if m in date_str:
                date_str = date_str.replace(m, months[m])
                return datetime.strptime(date_str, '%d %m %Y').date()

    for k, v in tool.data.items():
        error = False
        _dates = {}
        for el in to_convert:
            if not el in v:
                error = True
                continue

            if not isinstance(v[el], date):
                _date = convert_date(v[el])
                if not _date:
                    logger.error('Impossibile convertire {0} - {1}'.format(
                        v[el], k))
                    error = True
                    continue
                _dates[el] = _date

        if error:
            continue

        v.update(_dates)
        tool.data[k] = v


def upgrade_to_1005(context, logger=None):
    logger = getLogger(logger)
    logger.info(
        "Create openerp_order_number "
        "and openerp_order_number_db indexes"
    )
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'catalog')

    logger.info("Reindex created indexes")
    pc = getToolByName(context, 'portal_catalog')
    pc.reindexIndex('openerp_order_number', context.REQUEST)
    pc.reindexIndex('openerp_order_number_db', context.REQUEST)
