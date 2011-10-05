import urllib
import urlparse
import logging

import rdioconfig


class LinkShareException(Exception):

    def __init__(self, error_str):
        self.error_str = error_str

    def __str__(self):
        return repr(self.error_str)


class LinkShareHelper:

    DEEP_LINK_API_SCHEME = 'http'
    DEEP_LINK_API_NETLOC = 'getdeeplink.linksynergy.com'
    DEEP_LINK_API_PATH = 'createcustomlink.shtml'

    def __init__(self, token, merchant_id):
        self.token = token
        self.merchant_id = merchant_id

    def generate_link_simple(self, url):

        base = 'http://click.linksynergy.com/fs-bin/click'
        url = urllib.quote_plus(url)
        url = urllib.quote_plus(url)

        query = '%s?id=%s&subid=%s&offerid=%s&type=%s&tmpid=%s&RD_PARM1=%s' % (
            base, 'DUH1j*FWY7w', '0', '221756.1', '10', '7950', url)

        return query

    def generate_link(self, url):
        """Returns an affiliate deep-link for the given URL"""

        request_url = self._build_link(url)
        f = urllib.urlopen(request_url)
        response = f.read()

        if response.startswith("http://"):
            return response
        else:
            raise LinkShareException(response)

    def _build_link(self, url):
        """Builds a URL used to generate a LinkShare deep-link"""

        request_url = urlparse.ParseResult(scheme=self.DEEP_LINK_API_SCHEME,
                netloc=self.DEEP_LINK_API_NETLOC,
                path=self.DEEP_LINK_API_PATH,
                params='',
                query=self._generate_query(url),
                fragment='')

        result_link = urlparse.urlunparse(request_url)
        logging.debug('_build_link:%s' % result_link)
        return result_link

    def _generate_query(self, url):
        """Generates a query parameter to be passed to urlparse.urlunparse()"""

        query_str = "token=%s&mid=%s&murl=%s" % (self.token, self.merchant_id,
            url)

        logging.debug('_generate_query:%s', query_str)
        return query_str


def identical_test():
    src_link = 'http://www.rdio.com/artist/Mastodon/album/The_Hunter/'

    linkshare_helper = LinkShareHelper(rdioconfig.LINKSHARE_TOKEN,
        rdioconfig.LINKSHARE_MERCHANT_ID)

    simple_link = linkshare_helper.generate_link_simple(src_link)
    link = linkshare_helper.generate_link(src_link)
    if link == simple_link:
        print "Same!"
    else:
        print "Different!"


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    identical_test()
