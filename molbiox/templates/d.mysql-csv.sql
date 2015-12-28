SELECT
{% for col in columns -%}
    {{ col }}{% if not loop.last %}, {% endif %}
{%- endfor %}

INTO
    OUTFILE '{{ filename }}'
    FIELDS TERMINATED BY ','  OPTIONALLY ENCLOSED BY '"'
    LINES  TERMINATED BY '\n'
FROM {{ table }}
WHERE 1 = 1

{%- for k in restrictions %}
    and {{ k }} = '{{ restrictions[k] }}'
{%- endfor -%};
