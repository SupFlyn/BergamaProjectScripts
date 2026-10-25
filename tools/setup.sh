#!/bin/bash
# setup.sh: one-time set-up in a fresh cloud container (about 2 minutes).
# Gets the test inputs from the project folder: the run kit's Data/ files and a pickle of the survey file.
set -e
P=/mnt/project-files
pip install -q rhino3dm pyflakes 2>&1 | grep -v WARNING || true
mkdir -p /home/claude/kit && cd /home/claude/kit && unzip -q -o $P/run_kit_2026-10-25/Bergama_run_kit_2026-10-25.zip 'Data/*'
[ -f /home/claude/survey.pkl ] || python3 $(dirname $(realpath $0))/survey_to_pickle.py $P/Bergama_Altlik.3dm /home/claude/survey.pkl
echo "ready: BERGAMA_DATA=/home/claude/kit/Data BERGAMA_SURVEY=/home/claude/survey.pkl"
