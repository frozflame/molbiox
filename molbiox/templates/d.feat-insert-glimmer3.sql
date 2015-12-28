
INSERT INTO {{ table }}
  (strain, contig, orfkey, headpos, tailpos, orientation, glimmer_score)
VALUES
{% for r in records -%}
  ('{{strain}}', '{{r.contig}}', '{{r.orf}}', {{r.head}}, {{r.tail}}, {{r.frame>0 | int()}}, {{r.score}})
  {%- if not loop.last -%},{% else %};{%- endif %}
{% endfor %}
