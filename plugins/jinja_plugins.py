import json

from datasette import hookimpl


filter_registry = {}
global_registry = {}
test_registry = {}


def register_filter(f):
    filter_registry[f.__name__] = f


def register_global(f):
    global_registry[f.__name__] = f


def register_test(f):
    test_registry[f.__name__] = f


@hookimpl
def prepare_jinja2_environment(env):
    env.filters.update(filter_registry)
    env.tests.update(test_registry)
    env.globals.update({ name: f() for name, f in global_registry.items()})


@register_global
def site_info():
    with open("site_info.json") as f:
        return json.load(f)
