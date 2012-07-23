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
        dispatcher.connect(self.handle_item_saved,
                signal=signals.item_saved)

    def handle_link_extracted(self, url, link_num):
        log.msg("receive signal[link_extracted], %s, %s"\
            %(url, link_num))
        self.metainfo.save_extract_info(url, link_num)

    def handle_item_saved(self, item):
        log.msg("receive signal[item_saved], %s" %(item['url'],))
        self.pmengine.process(item)
