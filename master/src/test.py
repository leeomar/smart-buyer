#!/usr/bin/env python

import sys
sys.path.append("../../gen-py.twisted")

from scheduler.ttypes import Seed

s1 = Seed()
s2 = Seed()

seeds = set()
seeds.add(s1)
seeds.add(s2)
print seeds
