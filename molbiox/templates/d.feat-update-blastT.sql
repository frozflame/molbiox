UPDATE {{ table }} SET
  blast_tophit_name = '{{ rec["subject.title"] }}',
  blast_tophit_accession = '{{ rec["subject.acc"] }}',
  blast_tophit_evalue = '{{ rec["evalue"] }}',
  blast_tophit_identity = {{ rec["percent.identity"] }},
  blast_tophit_similarity = {{ rec["percent.positives"] }},
  blast_tophit_match = {{ rec["identical"] }}
WHERE
  strain = '{{ strain }}' and
  -- contig = '{{ contig }}' and
  orfkey = '{{ orf }}';

