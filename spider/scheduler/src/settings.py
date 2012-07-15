######################################
# Project Configuration
######################################
LOG_FILE = 'server.log'
LOG_DIR = '../log'

SERVER = {
    'name'  : 'MeMaster',
    'iface' : '127.0.0.1',
    'port'  : 9090,
}

######################################
#                                    #
# the following is log configuration #
#                                    #   
######################################
'''
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
    #LOG_FILENAME = os.path.join(os.path.dirname(__file__),'log/ifind_sync.log').replace('\\','/')
    #handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, 'midnight', 1, 5)
    handler = DailyRotatingFileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
'''
