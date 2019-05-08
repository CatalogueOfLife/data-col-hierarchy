# col-hierarchy
The CoL management classification with species estimates down to families.

## Preparation
Dumped from col _tree table.
Removed all names below family rank: 
genus, species, subspecies, variety, form

## SQL
creates the tree.txt:

```
\copy (WITH RECURSIVE x AS( SELECT taxon_id, name, rank, total_species_estimation, source, array[taxon_id] AS path FROM tree WHERE parent_id=0 UNION SELECT t.taxon_id, t.name, t.rank, t.total_species_estimation, t.source, (x.path || t.taxon_id) FROM tree t, x WHERE t.parent_id = x.taxon_id) SELECT repeat('  ', array_length(path,1)-1) || name || ' [' || rank || ']' || CASE total_species_estimation WHEN 0 THEN '' ELSE ' ' || total_species_estimation || ' ' || source END FROM x ORDER BY path) to 'tree.txt'
```


## Python dwca generator
requires `pip install openpyxl`