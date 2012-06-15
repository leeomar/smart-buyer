"""
This module contains general purpose URL functions not found in the standard
library.
"""
import re
import urlparse
import urllib
import types
import hashlib
import cgi

from scrapy.utils.python import unicode_to_str
from scrapy.utils.url import safe_url_string

def get_uid(url):
    """
        get the uid of the url
        algorithm:
        1) get 16 bytes (128 bits) md5, encoded by hex
        2) split the first 8 bytes and the last 8 bytes
        3) convert the two 8 bytes into int
        4) XOR the two 8 bytes
        5) encode the result by hex
    """
    # convert unicode to str (with encode utf-8)
    # this function is str safe, without double encode error
    url = unicode_to_str(url)
    if isinstance(url, types.StringType):
        # md5 is a string represents a 32bytes hex number
        md5 = hashlib.new("md5", url).hexdigest()
        first_half_bytes = md5[:16]
        last_half_bytes = md5[16:]

        # get the two long int
        first_half_int = int(first_half_bytes, 16)
        last_half_int = int(last_half_bytes, 16)

        # XOR the two long int, get a long int
        xor_int = first_half_int ^ last_half_int

        # convert to a hex string
        uid = "%x" % xor_int

        return uid
    else:
        raise Exception('cannot sign a no-string object:%s' % type(url))

ip_pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
def get_domain(url):
    """
        Note: this function is not perfect to get domain,
        which need a TLDs list to deal with like http://www.foo.com.au/
    """
    TLDs = ('cn',) # 'jp', 'uk', 'tw', 'us'
    host = urlparse.urlparse(url).hostname
    print host
    if host:
        if ip_pattern.match(host):
            return host

        #remove the TLDs
        suffix = None
        for tld in TLDs:
            if host.endswith(tld):
                suffix = tld
                host = '.'.join(host.split('.')[:-1])
                break

        # get domain
        if suffix:
            return '.'.join(host.split('.')[-2:]+[suffix,])
        else:
            return '.'.join(host.split('.')[-2:])
    else:
        raise Exception('fail parse hostname from %s' % url)

def canonicalize_url(url, keep_blank_values=True, keep_fragments=False, \
        encoding=None):
    """Canonicalize the given url by applying the following procedures:

    - sort query arguments, first by key, then by value
    - percent encode paths and query arguments. non-ASCII characters are
      percent-encoded using UTF-8 (RFC-3986)
    - normalize all spaces (in query arguments) '+' (plus symbol)
    - normalize percent encodings case (%2f -> %2F)
    - remove query arguments with blank values (unless keep_blank_values is True)
    - remove fragments (unless keep_fragments is True)

    The url passed can be a str or unicode, while the url returned is always a
    str.

    For examples see the tests in scrapy.tests.test_utils_url
    """

    url = unicode_to_str(url, encoding)
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    keyvals = cgi.parse_qsl(query, keep_blank_values)
    keyvals.sort()
    query = urllib.urlencode(keyvals)
    # strip is added by hewei
    path = safe_url_string(urllib.unquote(path).strip())
    fragment = '' if not keep_fragments else fragment
    return urlparse.urlunparse((scheme, netloc.lower(), path, params, query, fragment))
