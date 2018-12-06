import json

from jinja2 import contextfilter, contextfunction
from datasette import hookimpl


filter_registry = {}
global_registry = {}
global_func_registry = {}
test_registry = {}


class register:
    def __init__(self, registry):
        self.registry = registry

    def __call__(self, f):
        self.registry[f.__name__] = f
        return f


@hookimpl
def prepare_jinja2_environment(env):
    env.filters.update(filter_registry)
    env.tests.update(test_registry)
    env.globals.update(global_func_registry)
    env.globals.update({name: f() for name, f in global_registry.items()})


@register(global_registry)
def site_info():
    with open("site_info.json") as f:
        return json.load(f)


formatted_names = {
    "agency": "Agency code",
    "annual_salary": "Annual salary",
    "class_code": "Class code",
    "first_name": "First Name",
    "last_name": "Last Name",
    "middle_initial": "MI",
    "organization": "Organization",
    "other_earnings": "Other earnings",
    "overtime_earnings": "Overtime",
    "pay_rate": "Pay rate",
    "regular_earnings": "Regular earnings",
    "subtitle": "Subtitle",
    "suffix": "Suffix",
    "system": "System",
    "term_date": "Termination date",
    "ytd_gross_earnings": "2017 Gross Earnings",
}


@register(filter_registry)
def format_name(val):
    if val in formatted_names:
        return formatted_names[val]

    return val.replace("(numeric)", "", 1).replace("(dollars)", "", 1)


@register(filter_registry)
def format_name_long(val):
    val = format_name(val)
    if val == "MI":
        return "Middle Initial"
    return val


@register(filter_registry)
def format_money(val):
    try:
        numeric = float(val)
    except ValueError:
        return val

    return "${:,.2f}".format(numeric)


@register(filter_registry)
def format_numeric(val):
    try:
        numeric = float(val)
    except ValueError:
        return val

    return "{:,.0f}".format(numeric)


monetary_cols = {
    "annual_salary",
    "other_earnings",
    "overtime_earnings",
    "regular_earnings",
    "ytd_gross_earnings",
}


@register(global_func_registry)
def format_for(val, column):
    if column in monetary_cols or column.endswith("(dollars)"):
        return format_money(val)

    if column.endswith("(numeric)"):
        return format_numeric(val)

    return val


@register(test_registry)
def numeric(column):
    return (
        column in monetary_cols
        or column.endswith("(numeric)")
        or column.endswith("(dollars)")
    )
