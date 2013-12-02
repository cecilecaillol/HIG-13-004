
for chan in vhtt_zh cmb vhtt_wh vhtt_wh_had ett mtt mmt emt lltt llet llem llmt
do
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/90
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/95
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/100
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/105
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/110
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/115
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/120
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/125
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/130
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/135
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/140
   commentUncerts.py --drop-list='uncertainty-pruning-drop.txt' limits/$chan/145
done
