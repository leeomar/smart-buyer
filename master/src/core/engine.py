#!/usr/bin/env python
# coding: utf8
import sys
sys.path.append('../../gen-py.twisted')

from twisted.python import log
from scheduler.ttypes import SeedsPackage
from utils.reactor import CallLaterOnce

class CycleSeederEngine(object):
    name = 'CycleSeederEngine'

    def __init__(self, seed_service):
        self.seed_service = seed_service
        self.loop_calls = {}
        self.time_shared_seeds = {}
        self.de = set()

    def cancel(self):
        for key in self.loop_calls:
            self.loop_calls[key].cancel()
            del self.loop_calls[key]
        log.msg("cancel all items in CycleSeederEngine")

    def add_package(self, pkg):
        for seed in pkg.seeds:
            self.add(seed)

    def add(self, seed):
        if seed.seed_frequency == 0:
            return

        if seed.url in self.de:
            log.msg("%s alreay exist" % seed)
            return 

        if seed.seed_frequency in self.time_shared_seeds:
            self.time_shared_seeds[seed.seed_frequency].append(seed)
        else:
            self.time_shared_seeds[seed.seed_frequency] = [seed,]
            call = CallLaterOnce(self.excute, seed.seed_frequency)
            call.schedule(seed.seed_frequency)
            self.loop_calls[seed.seed_frequency] = call

        self.de.add(seed.url)
        log.msg('add %s to CycleSeederEngine' % seed)

    def excute(self, seed_frequency):
        pkg = SeedsPackage()
        pkg.ID = self.name
        pkg.seeds = self.time_shared_seeds[seed_frequency] 
        self.seed_service.add_seeds(self.name, pkg)
        #log.debug('excute auto add %s' % pkg)
        self.loop_calls[seed_frequency].schedule(seed_frequency)

    def status(self):
        return "CycleSeederEngine[%s]" % \
            ",".join(["%s" % self.loop_calls[key] for key in self.loop_calls])
