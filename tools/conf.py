import settings

class Settings(object):

    def __init__(self, values=None):
        self.values = values.copy() if values else {}
        self.global_defaults = settings

    def __getitem__(self, opt_name):
        if opt_name in self.values:
            return self.values[opt_name]
        return getattr(self.global_defaults, opt_name, None)

    def get(self, name, default=None):
        return self[name] if self[name] is not None else default

    def getbool(self, name, default=False):
        """
        True is: 1, '1', True
        False is: 0, '0', False, None
        """
        return bool(int(self.get(name, default)))

    def getint(self, name, default=0):
        return int(self.get(name, default))

    def getfloat(self, name, default=0.0):
        return float(self.get(name, default))

    def getlist(self, name, default=None):
        value = self.get(name)
        if value is None:
            return default or []
        elif hasattr(value, '__iter__'):
            return value
        else:
            return str(value).split(',')

settings = Settings()
######################################
#                                    #
# the following is log configuration #
#                                    #   
######################################
import os
import logging
import logging.handlers
LOGFILE = settings.get('LOG_FILE')
log = logging.getLogger('project')
if len( log.handlers ) == 0:
    log.setLevel(logging.DEBUG)
    LOG_FILENAME = os.path.join(os.path.dirname(__file__), \
            LOGFILE.replace('\\','/'))
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, 'midnight', 1, 5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: [%(module)s.%(funcName)s, Line:%(lineno)d] %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
