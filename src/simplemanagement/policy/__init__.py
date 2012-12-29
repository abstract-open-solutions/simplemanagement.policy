import re
from datetime import date, timedelta
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


DATE_REGEX = re.compile(
    r'^(?P<sign>\+|-)(?P<value>[0-9]+)(?P<quantifier>[dw])$'
)


def convert_date(value):
    today = date.today()
    values = DATE_REGEX.match(value).groupdict()
    delta_value = int(values['value'])
    if values['quantifier'] == 'd':
        delta = timedelta(days=delta_value)
    elif values['quantifier'] == 'w':
        delta = timedelta(days=(delta_value*7))
    if values['sign'] == '+':
        return today + delta
    else:
        return today - delta
