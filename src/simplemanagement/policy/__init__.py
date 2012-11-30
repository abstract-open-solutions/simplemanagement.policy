from DateTime import DateTime
from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('simplemanagement.policy')


def set_operatives(item):
    from collective.simplemanagement.structures import Resource
    data = eval(item)

    def create_operative(val):
        res = Resource()
        res.role = val[0]
        res.user_id = val[1]
        return res

    return [create_operative(i) for i in data]


def set_environments(item):
    from collective.simplemanagement.structures import Environment
    data = eval(item)

    def create_obj(val):
        res = Environment()
        res.name = val[0]
        res.env_type = val[1]
        res.url = val[2]

        return res

    return [create_obj(i) for i in data]


def set_milestones(item):
    from collective.simplemanagement.structures import Milestone
    data = eval(item)

    def create_obj(val):
        res = Milestone()
        res.name = val[0]
        res.status = val[1]

        return res

    return [create_obj(i) for i in data]
