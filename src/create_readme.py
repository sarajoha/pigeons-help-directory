import re
from itertools import groupby

import yaml
from jinja2 import Template

from utils import map_reduce, denormalize


def nest(seq, keys):
    if not keys:
        return seq
    first_key, *rest_keys = keys

    def keyfunc(x):
        return x[first_key]

    grouped = groupby(sorted(seq, key=keyfunc), key=keyfunc)
    result = {}
    for key, value in grouped:
        result[key] = nest(list(value), rest_keys)
    return result


def toc_link(link):
    return "#" + re.sub(r"[^a-zA-Z-]", "", link.lower().replace(" ", "-"))


def composed(f, g):
    return lambda x: f(g(x))


def unique_by_country(l):
    return {k["country"]: k for k in l}.values()


def remove_duplicate_country_entry(center):
    center["geo"] = unique_by_country(center["geo"])
    return center


with open("data.yaml", "r") as stream:
    try:
        DATA = yaml.safe_load(stream)

        # get Professional Help Centers
        DENORMALIZED_CENTERS = map_reduce(
            composed(denormalize, remove_duplicate_country_entry),
            DATA["professional_help_centers"],
        )
        NESTED_CENTERS = nest(DENORMALIZED_CENTERS, ["country", "type"])

        # get online Communities
        NESTED_COMMUNITIES = nest(DATA["communities"], ["language"])

        # Create Readme
        TEMPLATE = Template(open("template.md").read())

        README = TEMPLATE.render(
            professional_centers=NESTED_CENTERS,
            communities=NESTED_COMMUNITIES,
            rescue=DATA["rescue"],
            care=DATA["care"],
            toc_link=toc_link,
        )

        with open("../README.md", "w") as readme_file:
            readme_file.write(README)

    except yaml.YAMLError as error:
        print(error)
