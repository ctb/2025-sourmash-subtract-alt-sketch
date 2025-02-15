# 2025-sourmash-subtract-alt-sketch

Subtract everything in a picklist/database from a sketch. This has many
applications :).

For example, you could do a gather at k=51, and then subtract some or all
of the matches at k=21 before doing another gather.

## Usage

The command:
```
./sub.py <from_sketch> <match_db_or_manifest> -o <output> \
         --picklist <csvfile>:match_name:ident \
         -m <moltype> -k <ksize> -s <scaled>
```

will subtract sketches from `<match_db_or_manifest>` based on matching
identifiers in `<csvfile>` from `<from_sketch>` at the given
ksize/moltype/scaled, and save the results to `<output>`.

See `Snakefile.test` and `Snakefile.jean` for some actual command lines.

## Other use cases

In addition to the first use case mentioned above, there are a few other
use cases that come to mind.

You could do a gather against vertebrates at a scaled of 1m, and then
subtract them at a scaled of 1000 before doing another gather against
bacteria.

You could do an gather of a metagenome with euks, bacteria
and archeaa at one k-size/moltype, and then subtract the matches from
another before doing a viral gather.

You could do a prefetch of a metagenome against euks at k=51, and then
subtract all matches before doing a gather at k=21.
