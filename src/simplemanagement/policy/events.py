from datetime import date
from datetime import timedelta
from decimal import Decimal
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from .interfaces import IGenericReportingConfig
from . import MessageFactory as _


REPORTING_ITERATION_ID = 'reporting-iteration'
REPORTING_STORY_ID = 'reporting-story'


def create_generic_reporting_ui(obj, __):
    """Creates an iteration+story whose only use is to collect bookings
    (for projects that have an operative part that can't be tracked).
    """
    if not IGenericReportingConfig.providedBy(obj):
        return
    if not getattr(obj,'activate_generic_reporting', False):
        return
    _t = obj.translate
    if REPORTING_ITERATION_ID not in obj:
        obj.invokeFactory('Iteration', REPORTING_ITERATION_ID)
        iteration = obj[REPORTING_ITERATION_ID]
        iteration.title = _t(_(u"Reporting"))
        iteration.description = _t(_(u"Support iteration for generic reporting"))
        iteration.text = _t(_(u"Used to book generic activities on project. "))
        iteration.start = date.today()
        iteration.end = iteration.start + timedelta(180)
        # XXX: do we need to set proper start/end date?
        iteration.reindexObject()
        workflowTool = getToolByName(iteration, "portal_workflow")
        try:
            workflowTool.doActionFor(iteration, "activate")
        except WorkflowException:
            pass
    else:
        iteration = obj.get(REPORTING_ITERATION_ID)
    if REPORTING_STORY_ID not in iteration:
        iteration.invokeFactory('Story', REPORTING_STORY_ID)
        story = iteration[REPORTING_STORY_ID]
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
        # XXX: check if obj is correct, and not story
        # obj.estimate = Decimal("0.0")
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
