# Resources to help Pigeons

A curated list of rehab centers, avian veterinaries, sanctuaries and groups dedicated to help pigeons.

- [How to help a pigeon]({{toc_link("How to rescue a pigeon")}})
- [Vets, Rehab centers and Sanctuaries]({{toc_link("Avian Veterinaries, Rehab Centers and Sanctuaries")}})
- [Communities]({{toc_link("Online communities")}})

## How to rescue a pigeon

{% for resource in rescue -%}
- [{{resource.name}}]({{resource.link}})
{% endfor %}

## How to take care of a rescued pigeon

{% for resource in care -%}
- [{{resource.name}}]({{resource.link}})
{% endfor %}

## Avian Veterinaries, Rehab Centers and Sanctuaries

{% for country in professional_centers.keys() -%}
- [{{country}}]({{toc_link(country)}})
{% endfor -%}

{% for country, centersByCountry in professional_centers.items() -%}
### {{country}}

{% for type, centers in centersByCountry.items() -%}
#### {{type}}

| center | city |
| - | - |
{% for center in centers -%}
| [{{center.name}}]({{center.website}}) | {{center.city}} |
{% endfor %}

{% endfor %}

{% endfor %}

## Online communities

{% for language, groupByLanguage in communities.items() -%}
### {{language}}

| community | platform |
| - | - |
{% for group in groupByLanguage -%}
| [{{group.name}}]({{group.website}}) | {{group.platform}} |
{% endfor %}

{% endfor %}

---
Shoutout to [pogopaule](https://github.com/pogopaule), whose amazing repo [awesome-sustainability-jobs](https://github.com/pogopaule/awesome-sustainability-jobs) served as both inspiration and the base structure for this one :sparkles:
