
'''
user subscription rules will be stored in mongodb,
in the following format:
    {
        oid: ,
        url: ,
        uid: ,
        email: ,
        price: ,
        discount: ,
        xpath: ,
        frequency: ,
    }

    xpath:
    {
        oid: ,
        url: ,
        uid: ,
        xpath: ,
        frequency: ,
    }
'''
from utils.email import EmailClient

class Rule(object):
    COLLECTION = 'rules'

    def __init__(self, mongo):
        self.mongo = mongo

    def get(self, uid, price=None, discount=None):
        if not price and not discount:
            raise Exception('price and discount cannot be both None')
        
        key = 'price' if price else 'discount'
        value = price if price else discount
        rules = self.mongo.find(self.COLLECTION, 
            {'uid': uid, key : {'$lte': value}})

        emails = []
        for rule in rules:
            emails.appent(rule['email'])
        return emails

class PriceMonitorEngine(object):

    def __init__(self, mongo, mclient):
        self.rule = Rule(mongo) 
        self.mclient = mclient
    
    @classmethod
    def from_settings(cls, settings):
        mconf = settings.get('MAIL_SERVER')
        mclient = EmailClient(mconf['host'], 
            mconf['user'], mconf['pwd'],
            mconf['from'])

    #action will be triggered by 80 percent sale
    def process(self, item):
        pass

    def mail(self, to):
        pass
