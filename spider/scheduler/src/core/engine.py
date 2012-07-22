#!/usr/bin/env python
# coding: utf8
import sys
sys.path.append('../../gen-py.twisted')

from twisted.python import log
from scheduler.ttypes import SeedsPackage
from utils.reactor import CallLaterOnce
from utils.url import get_uid

class AutoseedingEngine(object):
    name = 'AutoseedingEngine'

    def __init__(self, seed_service):
        self.seed_service = seed_service
        self.loop_calls = {}
        self.timeslice_seeds = {} #maping 
        self.uid2timeslice = {} #maping uid <-> 

    def cancel(self):
        for key in self.loop_calls:
            self.loop_calls[key].cancel()
            del self.loop_calls[key]
        log.msg("cancel all items in AutoseedingEngine")

    def add_package(self, pkg):
        for seed in pkg.seeds:
            self.add(seed)

    def remove(self, url):
        uid = get_uid(url)
        timeslice = self.uid2timeslice(uid)
        self.timeslice_seeds[timeslice].remove(url)
        if len(self.timeslice_seeds[timeslice]) == 0:
            del self.timeslice_seeds[timeslice]
            self.loop_calls[timeslice].cancel()
            del self.loop_calls[timeslice]
            log.msg("cancel loop call, schedule interval: %s" % timeslice)
        log.msg('remove %s from AutoseedingEngine' % url) 

    def add(self, seed):
        if seed.seed_frequency == 0:
            return

        #if exit, remove the old one
        uid = get_uid(seed.url)
        if uid in self.uid2timeslice:
            if seed.seed_frequency == self.uid2timeslice[uid]:
                log.msg('duplicate seed to AutoseedingEngine, %s, ignore seed' % seed)
                return
            else:
                log.msg("%s exist, schedule interval, old: %s, new:%s" \
                        %(self.uid2timeslice[uid], seed.seed_frequency, seed.url))
                self.remove(seed.url)

        if seed.seed_frequency in self.timeslice_seeds:
            self.timeslice_seeds[seed.seed_frequency].append(seed)
        else:
            self.timeslice_seeds[seed.seed_frequency] = [seed,]
            call = CallLaterOnce(self.execute, seed.seed_frequency)
            call.schedule(seed.seed_frequency)
            self.loop_calls[seed.seed_frequency] = call

        self.uid2timeslice[uid] = seed.seed_frequency
        log.msg('add %s to AutoseedingEngine' % seed)

    def execute(self, seed_frequency):
        pkg = SeedsPackage()
        pkg.ID = self.name
        pkg.seeds = self.timeslice_seeds[seed_frequency] 
        self.seed_service.add_seeds(self.name, pkg)
        self.loop_calls[seed_frequency].schedule(seed_frequency)

    def status(self):
        return "AutoseedingEngine[%s]" % \
            ",".join(["%s" % self.loop_calls[key] for key in self.loop_calls])
