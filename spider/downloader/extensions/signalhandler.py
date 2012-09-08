#/bin/python
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log

from scrapy.conf import settings
from downloader import signals
from downloader.extensions.watcher.engine import PriceWatcherEngine
from .statistic import StatisticInfo
from .mysolr import MySolr

class SignalHandler(object):

    def __init__(self):
        self.pmengine = PriceWatcherEngine.from_settings(settings)
        self.statistic = StatisticInfo(settings.get('REDIS'))

        self.enable_solr = settings.get('ENABLE_SOLR')
        if self.enable_solr:
            self.mysolr = MySolr(settings.get('SOLR'))
    
        dispatcher.connect(self.handle_link_extracted,
                signal=signals.link_extracted)
        dispatcher.connect(self.handle_product_record_saved,
                signal=signals.product_record_saved)
        dispatcher.connect(self.handle_product_record_extracted,
                signal=signals.product_record_extracted)
        dispatcher.connect(self.handle_kele_record_saved, 
                signal=signals.kele_record_saved)

    def handle_link_extracted(self, url, link_num):
        log.msg("receive signal[link_extracted], %s, %s"\
            %(url, link_num))
        self.statistic.save_extract_info(url, link_num)

    def handle_product_record_saved(self, record):
        log.msg("receive signal[product_record_saved], %s" %(record,))
        self.statistic.record_saved(record)
        self.pmengine.process(record)
        '''
            save record to solr
        '''
        if self.enable_solr:
            self.mysolr.add(record)


    def handle_kele_record_saved(self, doc):
        if self.enable_solr:
            self.mysolr.add(doc)

    def handle_product_record_extracted(self, record):
        log.msg("receive signal[product_record_saved], %s" %(record['url'],))
        self.statistic.record_extracted(record)
