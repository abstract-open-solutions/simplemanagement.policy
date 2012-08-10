from Products.CMFPlone.utils import getToolByName
# -*- extra stuff goes here -*-
from collective.transmogrifier.transmogrifier import Transmogrifier


def load_content(context):
    if context.readDataFile('loadcontent_various.txt') is None:
        return
    portal = context.getSite()

    transmogrifier = Transmogrifier(portal)
    transmogrifier(u'load_content')
    return 'Imported content types...'


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
