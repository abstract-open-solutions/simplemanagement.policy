import oerplib
from zope.component import getUtility
from plone.registry.interfaces import IRegistry


class OpenerpConnector(object):
    """Basic connector to openerp
    Usage:

    >>> filters = [
    ...     ('state', '=', 'validate'),
    ...     ('type', '=', 'remove'),  # filter assegnazione permessi
    ...     ('date_from', '>=', self._convert_date(start)),
    ...     ('date_to', '<=', self._convert_date(end))
    ... ]

    >>> connector = OpenerpConnector()
    >>> user_id = connector.login()
    >>> brains = connector.search('hr.holidays', filters)
    [ ... ]

    """
    settings = None
    oerp = None

    def __init__(self, timeout=10, settings=None):
        if settings is not None:
            self.settings = settings
        else:
            if not self.settings:
                self.settings = self._settings

        if not self.oerp:
            self.oerp = oerplib.OERP(
                self.settings['openerp.host'],
                protocol='xmlrpc',
                port=self.settings['openerp.port'],
            )
            self.oerp.config['timeout'] = timeout

    @property
    def _settings(self):
        settings = {
            "openerp.host": None,
            "openerp.port": None,
            "openerp.user": None,
            "openerp.password": None,
            "openerp.database": None
        }
        registry = getUtility(IRegistry)
        for f in settings:
            settings[f] = registry[f]
        return settings

    def login(self):
        return self.oerp.login(
            self.settings['openerp.user'],
            self.settings['openerp.password'],
            self.settings['openerp.database']
        )

    def search(self, model, filters=[]):
        _ids = self.oerp.search(model, filters)
        return self.oerp.browse(model, _ids)
