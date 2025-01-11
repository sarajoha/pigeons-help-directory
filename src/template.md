# Resources to help Pigeons

A curated list of rehabs, vet, sactuaries, NGOS and social media accounts that help or appreciate pigeons.

-- organize per country and category
-- how to rescue or take care of pigeons
-- directory of vets and rehabs per country

## How to rescue a pigeon

{% for resource in rescue -%}
- [{{resource.name}}]({{resource.link}})
{% endfor %}

## How to take care of a rescued pigeon

{% for resource in care -%}
- [{{resource.name}}]({{resource.link}})
{% endfor %}
