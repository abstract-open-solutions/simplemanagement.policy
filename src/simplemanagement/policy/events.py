from decimal import Decimal
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from . import MessageFactory as _


REPORTING_STORY_ID = 'reporting'


def create_reporting_story(obj, __):
    """Creates a story whose only use is to collect bookings
    (for projects that have an operative part that can't be tracked).
    """
    _t = obj.translate
    if REPORTING_STORY_ID not in obj:
        obj.invokeFactory('Story', REPORTING_STORY_ID)
        story = obj[REPORTING_STORY_ID]
        story.title = _t(_(u"Reporting"))
        story.description = _t(_(u"Support content for reporting"))
        story.text = _t(_(u"Here is where bookings must be inserted "
                          u"when this project is being used "
                          u"for reporting only.\n\n"
                          u"Insert bookings here if:\n\n"
                          u" - This project is in maintenance mode\n"
                          u" - This project is small\n"
                          u" - The project's activities are not tracked here "
                          u"via stories "
                          u"(but they are tracked via tickets, "
                          u"or external systems)\n\n"
                          u"*Do not* insert bookings here if:\n\n"
                          u" - There are open iterations and stories\n\n"))
        obj.estimate = Decimal("0.0")
        assigned_to = story.assigned_to if story.assigned_to is not None else []
        operatives = obj.operatives if obj.operatives is not None else []
        for operative in operatives:
            if operative.user_id not in assigned_to:
                assigned_to.append(operative.user_id)
        story.assigned_to = assigned_to
        story.reindexObject()
        workflowTool = getToolByName(story, "portal_workflow")
        try:
            workflowTool.doActionFor(story, "start")
        except WorkflowException:
            pass
