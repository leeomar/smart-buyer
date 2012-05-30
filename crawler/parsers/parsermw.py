#/bin/python
#coding: utf-8

from scrapy import log
from scrapy.utils.misc import load_object
from crawler.logobj import LogableObject
from crawler.parsers.basicparser import BasicLinkInfo, ReturnStatus

class ParserMiddlewareManager(LogableObject):
    component_name = 'spider parser middleware manager'

    def __init__(self, parsers, spider=None):
        super(ParserMiddlewareManager, self).__init__(spider)
        self.parsers = parsers

    @classmethod
    def from_settings(cls, settings, spider=None):
        parser_classes = settings.get("SPIDER_PARSERS", ()) 
        parsers = []
        for clspath in parser_classes:
            parser_cls = load_object(clspath)
            if hasattr(parser_cls, 'from_settings'):
                parser_obj = parser_cls.from_settings(settings)
            else:
                parser_obj = parser_cls()
    
            parsers.append(parser_obj)

        enabled = [x.__class__.__name__ for x in parsers]
        log.msg("Enabled %ss: %s" % (cls.component_name, ", ".join(enabled)), \
           level=log.DEBUG)
        return cls(parsers, spider)

    """
    def get_parser(self, parser_cls):
        print self.parsers
        for parser in self.parsers:
            print type(parser)
            if isinstance(parser, parser_cls):
                return parser

        return None
    """
    def process_response(self, response, spider):
        basic_link_info = BasicLinkInfo.from_response(response)
        self.log("%s" % basic_link_info, level=log.DEBUG)

        ret_status = None
        for parser in self.parser_manager.parsers:
            ret_status = parser.parse(response, basic_link_info, spider)
            if ret_status == ReturnStatus.stop_it:
                break

        if ret_status != ReturnStatus.stop_it:
            self.log('ignore unknow response: %s' % type(response), level=log.ERROR)
