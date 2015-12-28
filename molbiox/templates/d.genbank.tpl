{%- set space = ' ' -%}
{%- set endl = '\n' -%}
FEATURES             Location/Qualifiers
{% for feat in gbdict['features'] -%}
    {{ space * 5 + feat['feattype'] + space * (16 - feat['feattype'].__len__()) }}{{ feat['location'] + endl }}
    {%- for qualline in feat['quallines'] -%}
        {%-  for subqualline in wrap('/' + qualline, 58) -%}
            {{ space * 21 + subqualline + endl }}
        {%-  endfor %}
    {%- endfor %}
{%- endfor %}
ORIGIN
{%  for idx in range(0, gbdict['sequence'].__len__(), 60) -%}
    {{ '{0:>9}'.format(idx + 1) }} {{ space.join(wrap(gbdict['sequence'][idx : idx + 60], 10)) }}
{%  endfor %}