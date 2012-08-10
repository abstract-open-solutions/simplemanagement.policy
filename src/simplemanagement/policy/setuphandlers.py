from Products.CMFPlone.utils import getToolByName
# -*- extra stuff goes here -*-


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
