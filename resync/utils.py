"""
util.py: A collection of common util functions used in source and/or client.

"""

import base64
import hashlib
from functools import partial
from logging import Formatter
from datetime import datetime


class UTCFormatter(Formatter):
    # based on http://bit.ly/T2n3Xk
    def formatTime(self, record, datefmt=None):
        timestamp = record.created
        return datetime.utcfromtimestamp(timestamp).isoformat() + 'Z'

"""Compute digests for ResourceSync

These are all base64 encoded according to the rules of
http://www.ietf.org/rfc/rfc4648.txt

MD5

ResourceSync defined to be the same as for Content-MD5 in HTTP,
http://www.ietf.org/rfc/rfc2616.txt which, in turn, defined the
digest string as the "base64 of 128 bit MD5 digest as per RFC 1864"
http://www.ietf.org/rfc/rfc1864.txt

Unfortunately, RFC1864 is rather vague and contains only and example
which doesn't use encoding characters for 62 or 63. It points to
RFC1521 to describe base64 which is explicit that the encoding alphabet
is [A-Za-z0-9+/] with = to pad.

The above corresponds with the alphabet of "3. Base 64 Encoding" in RFC3548
http://www.ietf.org/rfc/rfc3548.txt
and not the url safe version, "Base 64 Encoding with URL and Filename Safe
Alphabet" which replaces + and / with - and _ respectively.

This is the same as the alphabet of "4. Base 64 Encoding" in RFC4648
http://www.ietf.org/rfc/rfc4648.txt.

This algorithm is implemented by base64.standard_b64encode() or
base64.b64encode() with no altchars specified. Available in python2.4 and
up [http://docs.python.org/library/base64.html]
"""

"""

   The Content-MD5 header field has been removed because it was
   inconsistently implemented with respect to partial responses.
   http://tools.ietf.org/html/rfc7231#appendix-B [Page 92]
"""

def compute_md5_for_string(string):
    """Compute MD5 digest over some string payload"""
    return base64.b64encode(hashlib.md5(
            string.encode('utf-8')).digest()).decode('utf-8')


# can only read utf-8 encoded rs.
def old_compute_md5_for_file(filename, block_size=2**14):
    """Compute MD5 digest for a file

    Optional block_size parameter controls memory used to do MD5 calculation.
    This should be a multiple of 128 bytes.
    """
    f = open(filename, 'r', encoding='utf-8')
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data.encode('utf-8'))
    f.close()
    return base64.b64encode(md5.digest()).decode('utf-8')

def compute_md5_for_file(filename, block_size=2**14):
    """Compute MD5 digest for a file

    Optional block_size parameter controls memory used to do MD5 calculation.
    This should be a multiple of 128 bytes.
    """
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, block_size), b''):
            d.update(buf)

    return base64.b64encode(d.digest()).decode('utf-8')