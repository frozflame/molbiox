UPDATE {{ table }} SET
  pfam_tophit_name = '{{ name }}',
  pfam_tophit_accession = '{{ accession }}',
  pfam_tophit_evalue = '{{ evalue }}'
WHERE
  strain = '{{ strain }}' and
  contig = '{{ contig }}' and
  orfkey = '{{ orfkey }}';


