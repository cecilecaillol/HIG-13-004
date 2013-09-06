#! /bin/env python

import os
import glob
import re

mine   = os.path.join(os.getcwd(), 'limits/ltt')
adrian = os.path.join(os.environ['CMSSW_BASE'], 'src/auxiliaries/datacards/collected/vhtt/tmp/fakecorr2-2011counting-std-vTauTauVisMass_cut-Full-rebin40-scale1-systall-shapeAll/datacards/')

mycards = glob.glob(os.path.join(mine,'???/*.txt'))
regex   = re.compile('.*ltt/(?P<mass>[0-9]+)/vhtt_(?P<category>[0-9])_(?P<period>[0-9]TeV).txt') #.../ltt/115/vhtt_2_7TeV.txt
for card in mycards:
    m = regex.match(card)
    if m:
        adrian_card = os.path.join(adrian, 'combined-{PERIOD}/{MASS}/datacard_{PERIOD}.txt'.format(PERIOD=m.group('period'), MASS=m.group('mass')))
        if os.path.isfile(adrian_card):
            command = 'diff %s %s' % (card, adrian_card)
            print command
            os.system(command)
        else:
            print 'no datacard match for %s' % card
    else:
        print 'no regex match for %s' % card
    print '\n\n\n'
            
