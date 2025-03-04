# Querying a DBRetina index

Query a DBRetina index with a set of groups (provided as a single-column file or cluster IDs in a DBRetina cluster file).

```
Usage: DBRetina query [OPTIONS]

  Query DBRetina index.

  Detailed description:

      Query a DBRetina index with a set of groups (provided as a single-column
      file or cluster IDs in a DBRetina cluster file). Output each feature and
      the associated supergroups.

  Examples:

      1- groups file                    | DBRetina query -i index_prefix -g
      groups_file -o output_prefix

      2- clusters file with cluster IDs | DBRetina query -i index_prefix
      --clusters-file clusters_file --cluster-ids 1,2,3 -o output_prefix



Options:
  -i, --index-prefix TEXT  index file prefix  [required]
  -g, --groups-file PATH   single-column supergroups file
  --clusters-file PATH     DBRetina clusters file
  --cluster-ids TEXT       comma-separated list of cluster IDs
  -o, --output TEXT        output file prefix  [required]
  --help                   Show this message and exit.
```

## Command arguments


<span class="cmd"> -i, --index-prefix TEXT  Index file prefix  [required] </span>

This is the user-defined prefix that was used in the indexing step.

<span class="cmd"> -g, --groups-file PATH    single-column supergroups file </span>

This will filter out all pairwise similarities that are between supergroups that are not in the provided groups file. The groups file is a single-column file that contains the names of the supergroups to be included in the filtering.

<span class="cmd"> --cluster-ids TEXT        comma-separated list of cluster IDs </span>

The cluster IDs selected from the clusters file. This argument is only used if the clusters file is not provided.

<span class="cmd"> -o, --output TEXT        output file prefix  [required] </span>

The output prefix that should be unique for this query.

---

## Output files format


<!-- TODO: Implement later -->
<!-- <span class="cmd"> {output_prefix}_features_count_per_group.tsv </span>

A TSV file containing two columns, the first column is the supergroup name and the second column is the number of features that are contained in that supergroup, and the third column is a PIPE-separated list of supergroups from the user query that are associated with the feature in the first column. -->

<span class="cmd"> {output_prefix}_feature_to_groups.tsv </span>

A three-columns TSV file containing the feature name, the number of supergroups associated with that feature, and a PIPE-separated list of supergroups associated with that feature.

<!-- TODO: Fix later -->
<!-- <span class="cmd"> {output_prefix}_features_count_per_group_histogram.png </span>

A histogram plot showing the distribution of the number of features per supergroup. -->