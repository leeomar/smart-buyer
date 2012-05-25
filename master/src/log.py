#/bin/python

######################################
#                                    #
# the following is log configuration #
#                                    #   
######################################
import os
import logging
import logging.handlers
from log_rotate import DailyRotatingFileHandler

LOGFILE = "../log/server.log" 
log = logging.getLogger('project')
if len( log.handlers ) == 0:
    log.setLevel(logging.DEBUG)
    LOG_FILENAME = os.path.join(os.path.dirname(__file__), \
            LOGFILE.replace('\\','/'))
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, 'midnight', 1, 5)
    #handler = DailyRotatingFileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: [%(module)s.%(funcName)s, Line:%(lineno)d] %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
