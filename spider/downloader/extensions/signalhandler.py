#/bin/python
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log

from scrapy.conf import settings
from downloader import signals
from downloader.extensions.watcher.engine import PriceWatcherEngine
from .meta import GoodsMetaInfo

class SignalHandler(object):

    def __init__(self):
        self.pmengine = PriceWatcherEngine.from_settings(settings)
        self.metainfo = GoodsMetaInfo(settings.get('REDIS'))

        dispatcher.connect(self.handle_link_extracted,
                signal=signals.link_extracted)
        dispatcher.connect(self.handle_product_record_saved,
                signal=signals.product_record_saved)
        dispatcher.connect(self.handle_product_record_extracted,
                signal=signals.product_record_extracted)

    def handle_link_extracted(self, url, link_num):
        log.msg("receive signal[link_extracted], %s, %s"\
            %(url, link_num))
        self.metainfo.save_extract_info(url, link_num)

    def handle_product_record_saved(self, record):
        log.msg("receive signal[product_record_saved], %s" %(record['url'],))
        self.metainfo.record_saved(record)
        self.pmengine.process(record)

    def handle_product_record_extracted(self, record):
        log.msg("receive signal[product_record_saved], %s" %(record['url'],))
        self.metainfo.record_extracted(record)

