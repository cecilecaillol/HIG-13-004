#! /bin/env python

import sys
import re
import os

def is_other_signal_shape_uncert(x):
 if not x.startswith('CMS_vhtt_'): return False
 if not 'WH' in x: return False
 return 'WH%d' % mass not in x

fpath = sys.argv[-1]
fname = os.path.basename(fpath)
fname_format = re.compile(r'(?P<channel>[a-zA-Z]+)_(?P<category>[0-9]+)_(?P<period>[0-9]+TeV)-(?P<mass>[0-9]+).txt')
m = fname_format.match(fname)
if not m:
    raise Exception('filename %s not in the proper format' % fname)

mass = int(m.group('mass'))
replaced_datacard = ''.join([line for line in open(fpath).readlines() if line == '' or not is_other_signal_shape_uncert(line.split()[0])])
open(fpath, 'w').write(replaced_datacard)
