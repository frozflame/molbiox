

DROP TABLE if EXISTS mbz_t1_features;
CREATE TABLE mbz_t1_features (
  ident INTEGER PRIMARY KEY AUTO_INCREMENT,

  strain CHAR(16)   NOT NULL,
  contig CHAR(255)  NOT NULL,
  orfkey CHAR(128)  NOT NULL,

  headpos INTEGER NOT NULL,
  tailpos INTEGER NOT NULL,

  orientation BOOL NOT NULL,
  glimmer_score NUMERIC,

  pfam_tophit_name      CHAR(128),
  pfam_tophit_accession CHAR(32),
  pfam_tophit_evalue    CHAR(32),

  blast_tophit_name         CHAR(255),
  blast_tophit_accession    CHAR(255),
  blast_tophit_evalue       CHAR(255),
  blast_tophit_identity     INTEGER,
  blast_tophit_similarity   INTEGER,
  blast_tophit_match        INTEGER,

  shortname CHAR(16),
  gccontent INTEGER
  --  n / 1000
);


DROP TABLE IF EXISTS mbz_t1_target_contigs;
CREATE TABLE mbz_t1_target_contigs (

  ident     INTEGER PRIMARY KEY,
  length    INTEGER,
  title     CHAR(255),
  source    CHAR(16) UNIQUE,
  hashsum   CHAR(40) UNIQUE
);