#/bin/python
#from pydispatch import dispatcher
from scrapy.xlib.pydispatch import dispatcher
from signals import discount_signal

def handle_specific_event( sender, moo):
    """Handle a simple event, requiring a "moo" parameter"""
    print 'Specialized event for %(sender)s moo=%(moo)r'%locals()

dispatcher.connect( handle_specific_event, signal=discount_signal, sender=dispatcher.Any,  )

first_sender = object()
dispatcher.send( signal=discount_signal, sender=first_sender, moo={'price': 1, 'url': 'a.url'})
