#!/usr/bin/env python3

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

import argparse
import json
import sys

import pyld.jsonld  # type: ignore


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("framed_jsonld", help="Output graph")
    parser.add_argument("frame_jsonld", help="Frame file")
    parser.add_argument("data_jsonld", help="Input JSON-LD graph")
    args = parser.parse_args()
    with open(args.frame_jsonld, "r") as in_fh:
        frame = json.load(in_fh)
    with open(args.data_jsonld, "r") as in_fh:
        json_input = json.load(in_fh)
    with open(args.framed_jsonld, "w") as out_fh:
        framed = pyld.jsonld.frame(json_input, frame)
        print(json.dumps(framed), file=out_fh)


if __name__ == "__main__":
    main()
