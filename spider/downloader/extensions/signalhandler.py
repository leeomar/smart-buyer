#/bin/python
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log

from scrapy.conf import settings
from downloader import signals
from downloader.monitor.engine import PriceMonitorEngine
from .meta import GoodsMetaInfo

class SignalHandler(object):

    def __init__(self):
        self.pmengine = PriceMonitorEngine.from_settings(settings)
        self.metainfo = GoodsMetaInfo(settings.get('REDIS'))

        dispatcher.connect(self.handle_item_extracted,
                signal=signals.item_extracted)
        dispatcher.connect(self.handle_item_saved,
                signal=signals.item_saved)

    def handle_item_extracted(self, url, item_num):
        log.msg("receive signal[item_extracted], %s, %s"\
            %(url, item_num))
        self.metainfo.save_extract_info(url, item_num)

    def handle_item_saved(self, item):
        log.msg("receive signal[item_saved], %s, %s" %(item.url,))
        self.pmengine.process(item)
