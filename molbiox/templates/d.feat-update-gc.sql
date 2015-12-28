UPDATE {{ table }} SET
  gccontent = {{ gc }}
WHERE
  strain = '{{ strain }}' and
  contig = '{{ contig }}' and
{% if head %}  headpos = {{ head }} and {% endif %}
{% if tail %}  tailpos = {{ tail }} and {% endif %}
  orfkey = '{{ orfkey }}';


