import pkg_resources
from Products.CMFPlone.utils import getToolByName

try:
    pkg_resources.get_distribution('collective.transmogrifier')
except pkg_resources.DistributionNotFound:
    HAS_TRANSMOGRIFIER = False
else:
    from collective.transmogrifier.transmogrifier import Transmogrifier
    HAS_TRANSMOGRIFIER = True


def create_users(context):
    if context.readDataFile('loadcontent_various.txt') is None:
        return

    portal = context.getSite()
    test_users = [
        ('employee1', 'employee1', 'employees'),
        ('employee2', 'employee2', 'employees'),
        ('pm1', 'pm1', 'PM'),
        ('customer', 'customer', None),
    ]

    for username, password, group in test_users:
        if username not in portal.acl_users.getUserIds():
            try:
                portal.portal_registration.addMember(username, password)
                if group:
                    portal.portal_groups.addPrincipalToGroup(username, group)
            except ValueError:
                logger.warn('The login name "%s" is not valid.' % username)
            except KeyError:
                logger.warn('The group "%s" is not valid.' % group)
    return 'Users created'


def load_content(context):
    if context.readDataFile('loadcontent_various.txt') is None:
        return
    portal = context.getSite()
    if HAS_TRANSMOGRIFIER:
        transmogrifier = Transmogrifier(portal)
        transmogrifier(u'load_content')
        return 'Imported content types...'
    return 'Please install collective.transmogrifier to use this import step'


def disable_cmfedition_versioning(portal):
    """Removing default versionable content types
    """
    portal_repository = getToolByName(portal, 'portal_repository')
    portal_repository.setVersionableContentTypes([])


def limit_history_versions(portal):
    """Limit number of history items per content
    """
    portal_purgepolicy = getToolByName(portal, 'portal_purgepolicy')
    portal_purgepolicy.maxNumberOfVersionsToKeep = 2


def import_various(context):
    if context.readDataFile('policy_various.txt') is None:
        return

    site = context.getSite()
    limit_history_versions(site)
    # decomment this line to remove default versioning policies
    # disable_cmfedition_versioning(site)
