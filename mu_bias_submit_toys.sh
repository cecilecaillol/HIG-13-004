#!/bin/bash


#DIRS="limits/mmt/125 limits/emt/125 limits/eet/125 limits/mtt/125 limits/ett/125 limits/vhtt_wh/125 limits/vhtt_wh_had/125 limits/vhtt_zh/125 limits/cmb/125"
DIRS="limits/mmt/125 limits/mmt_nofakes/125 limits/mmt_7TeV/125 \
    limits/mmt_8TeV/125 limits/mmt_8TeV_low/125 limits/mmt_8TeV_highscaled/125 \
    limits/mmt_8TeV_high/125 limits/emt/125 limits/vhtt_wh/125 limits/eet/125 \
    moriond/llt/125 moriond/mmt/125 moriond/emt/125"


for i in `seq 200`; do
    lxb-limit.py --condor --name="condor_toys_$i" \
        --limit-options="--max-likelihood-toys --stable --rMin -25 --rMax 25 --toys 100" \
        $DIRS
done

ls condor_toys_*sh | xargs -n 1 condor_submit

limit.py --max-likelihood --stable --rMin -15 --rMax 15 $DIRS &> /dev/null

limit.py --likelihood-scan --points 300 --rMin -15 --rMax 10 $DIRS &> /dev/null
