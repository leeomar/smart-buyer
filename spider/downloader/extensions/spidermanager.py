"""
create a spider or re-use existing spiders with different settings
"""

from scrapy import log
from scrapy.spidermanager import SpiderManager
from downloader.spiders.default import DefaultSpider

class MySpiderManager(SpiderManager):
    loaded = True
    
    def create(self, spider_name, **kwargs):
        if spider_name not in self._spiders:
            log.msg("create spider[%s]" % spider_name, level=log.INFO)
            self._spiders[spider_name] = DefaultSpider(spider_name, **kwargs)
        
        else:
            #===================================================================
			# self._spiders[spider_name].reset(
			#	spider_kwargs.get('seed_file'),
			#	spider_kwargs.get('batch_size'),
			#	spider_kwargs.get('download_delay')
			#	)
			#===================================================================
            log.msg("spider[%s] already exists!" % spider_name, level=log.ERROR)
        
        return self._spiders[spider_name]
