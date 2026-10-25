#!/bin/bash
# chain.sh <scripts_dir> <out_dir> : runs the 8 scripts offline in run-guide order (stub Rhino, frozen clock).
# Data files: $BERGAMA_DATA (default: the kit's Data folder unzipped at ~/kit/Data).
export BERGAMA_SURVEY=${BERGAMA_SURVEY:-/home/claude/survey.pkl}
T=$(dirname $(realpath $0)); D=$(realpath $1); H=$(realpath -m $2); DATA=${BERGAMA_DATA:-/home/claude/kit/Data}
rm -rf $H; mkdir -p $H/Downloads/Bergama/Data; cp $DATA/* $H/Downloads/Bergama/Data/
for s in zone_base masterplan water_balance board city_link agriculture_alternatives water_board proposal_sections; do
  f=$(ls $D/bergama_${s}_v*.py $D/selinus_${s}_v*.py 2>/dev/null | head -1)
  ( cd $H && timeout 1500 python3 -I $T/run_gh.py $f $H > $H/$s.stdout 2>&1 ); echo "$s rc=$? $(grep '#LOG#' $H/$s.stdout | cut -c1-200)"
done
