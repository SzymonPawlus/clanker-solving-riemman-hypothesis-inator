#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python3 analyze.py \
  ../circle-packing-search/out/n08.json \
  ../circle-packing-search/out/n11.json \
  ../circle-packing-search/out/n13.json
python3 -m unittest discover -s tests -v
