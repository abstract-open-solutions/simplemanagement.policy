import logging


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
