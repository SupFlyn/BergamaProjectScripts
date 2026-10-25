#!/bin/bash
# chain.sh <scripts_dir> <out_dir> : runs the scripts offline in run-guide order (fake Rhino, frozen clock).
#   $BERGAMA_DATA   the run kit's Data/ folder         (default /home/claude/kit/Data; tools/setup.sh makes it)
#   $BERGAMA_SURVEY pickle of Bergama_Altlik.3dm       (default /home/claude/survey.pkl)
#   $STEPS          which scripts, in this order        (default: all 8)
#   $KEEP=1         keep the out_dir (re-run some STEPS on top of an earlier run)
#   $SEED_CACHE     an earlier run folder: its cached/ is copied in first (the site board takes ~40 min cold)
export PYTHONHASHSEED=0   # same set/dict order in every run
export BERGAMA_SURVEY=${BERGAMA_SURVEY:-/home/claude/survey.pkl}
T=$(dirname $(realpath $0)); D=$(realpath $1); H=$(realpath -m $2); DATA=${BERGAMA_DATA:-/home/claude/kit/Data}
STEPS=${STEPS:-"zone_base masterplan water_balance board city_link agriculture_alternatives water_board proposal_sections"}
[ -z "$KEEP" ] && rm -rf $H; mkdir -p $H/Downloads/Bergama/Data; cp $DATA/* $H/Downloads/Bergama/Data/
[ -n "$SEED_CACHE" ] && cp -r $(realpath $SEED_CACHE)/Downloads/Bergama/cached $H/Downloads/Bergama/
for s in $STEPS; do
  f=$(ls $D/bergama_${s}_v*.py $D/selinus_${s}_v*.py 2>/dev/null | head -1)
  ( cd $H && timeout 7200 python3 -I $T/run_gh.py $f $H > $H/$s.stdout 2>&1 ); echo "$s rc=$? $(grep '#LOG#' $H/$s.stdout | cut -c1-200)"
done
