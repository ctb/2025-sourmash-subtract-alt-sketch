#! /usr/bin/env python
import argparse
import sourmash
import sys

from sourmash.cli.utils import add_picklist_args
from sourmash import sourmash_args


def main():
    p = argparse.ArgumentParser()
    p.add_argument('from_sketches')
    p.add_argument('match_sketches')
    p.add_argument('-m', '--moltype', default='DNA',
                   help='subtract at this moltype')
    p.add_argument('-k', '--ksize', default=31, type=int,
                   help='subtract at this ksize')
    p.add_argument('-s', '--scaled', default=1000, type=float,
                   help='downsample to this scaled before subtracting')
    p.add_argument('-o', '--output-sketches', help='save sketches here',
                   required=True)
    add_picklist_args(p)
    args = p.parse_args()

    picklist = sourmash_args.load_picklist(args)
    assert picklist is not None, "ERROR: must provide picklist"
    db = sourmash.load_file_as_index(args.match_sketches)

    print(f"loaded {len(db)} total sketches from db '{args.match_sketches}'")
    db = db.select(ksize=args.ksize, moltype=args.moltype, picklist=picklist)
    print(f"after selection at k={args.ksize}/{args.moltype}, {len(db)} left")
    sourmash_args.report_picklist(args, picklist)

    print(f"now loading from_sketch from '{args.from_sketches}'")
    from_sketches = sourmash.load_file_as_index(args.from_sketches)
    from_sketches = from_sketches.select(ksize=args.ksize, moltype=args.moltype)
    from_sketches = list(from_sketches.signatures())
    assert len(from_sketches) == 1, len(from_sketches)

    from_ss = from_sketches[0]
    from_mh = from_ss.minhash.downsample(scaled=args.scaled)
    from_mh_flat = from_mh.flatten()
    merged_isect = from_mh_flat.copy_and_clear()

    print('calculating merged intersections...')
    n = 0
    for n, sub_ss in enumerate(db.signatures(), start=1):
        if n and n % 10 == 0:
            print(f"\r\033[K... {n} of {len(db)}\r", end="")
        sub_mh = sub_ss.minhash.flatten().downsample(scaled=from_mh.scaled)
        isect = sub_mh.intersection(from_mh_flat)
        merged_isect += isect

    print('removing!')
    from_mh = from_mh.to_mutable()        
    from_mh.remove_many(merged_isect)

    n_orig = len(from_ss.minhash)
    n_remaining = len(from_mh)
    p_removed = (n_orig - n_remaining) / n_orig * 100
    print(f"removed {n} sketches total; removed {n_orig - n_remaining} hashes ({p_removed:.1f}%).")

    new_ss = sourmash.SourmashSignature(from_mh, name=from_ss.name)
    with sourmash_args.SaveSignaturesToLocation(args.output_sketches) as save:
        save.add(new_ss)


if __name__ == '__main__':
    sys.exit(main())
