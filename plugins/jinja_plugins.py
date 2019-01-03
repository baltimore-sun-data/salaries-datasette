import json
import os
from urllib import parse

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


@hookimpl
def render_cell(value, column):
    return format_for(value, column)


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
    "ytd_gross_earnings": "Gross Yearly Earnings",
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

    return "${:,.0f}".format(numeric)


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


_vue_manifest = None


def load_vue_manifest():
    global _vue_manifest
    if _vue_manifest is not None:
        return _vue_manifest

    manifest_file = os.environ.get("MANIFEST_FILE")
    if not manifest_file:
        _vue_manifest = False
        return _vue_manifest

    with open(manifest_file) as f:
        _vue_manifest = json.load(f)

    return _vue_manifest


@register(global_registry)
def is_vue_dev():
    return not load_vue_manifest()


@register(filter_registry)
def vue_url(entry):
    manifest = load_vue_manifest()
    if not manifest:
        return parse.urljoin("http://localhost:9002/static/", entry)

    return manifest.get(entry) or ""


@register(filter_registry)
@contextfilter
def abs_url(context, url_path):
    base_url = context["site_info"]["baseURL"]
    return parse.urljoin(base_url, url_path)


@register(global_func_registry)
@contextfunction
def get_path(context):
    path = "/"
    url_json = context.resolve("url_json")
    if url_json:
        path = url_json.replace(".json", "", 1)
    return path


@register(global_func_registry)
@contextfunction
def get_absolute_url(context):
    return abs_url(context, get_path(context))
