#/bin/python

from scrapy.xlib.pydispatch import dispatcher
from scrapy import log

from crawler import signals

class SignalHandler(object):

    def __init__(self):
        dispatcher.connect(self.handle_item_extracted,
                signal=signals.item_extracted)
        dispatcher.connect(self.handle_item_saved,
                signal=signals.item_saved)

    def handle_item_extracted(self, url, item_num):
        log.msg("receive signal[item_extracted], %s, %s"\
            %(url, item_num))

    def handle_item_saved(self, url, price, name, cat):
        log.msg("receive signal[item_saved], %s, %s, %s"\
            %(url, price, name,))
