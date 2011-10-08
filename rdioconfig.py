from ConfigParser import SafeConfigParser
import codecs
import os


class RdioConfig:

    RDIO_SECTION_NAME = 'rdio'
    LINKSHARE_SECTION_NAME = 'linkshare'
    DOWNLOADER_SECTION_NAME = 'rdio-downloader'

    def __init__(self, config_path):
        self.parser = SafeConfigParser()

        with codecs.open(config_path, 'r', encoding='utf-8') as f:
            self.parser.readfp(f)

    def get_rdio_key(self):
        return self.parser.get(self.RDIO_SECTION_NAME, 'consumer_key')

    def get_rdio_secret(self):
        return self.parser.get(self.RDIO_SECTION_NAME, 'consumer_secret')

    def get_linkshare_key(self):
        return self.parser.get(self.LINKSHARE_SECTION_NAME, 'token')

    def get_linkshare_merchant_id(self):
        return self.parser.get(self.LINKSHARE_SECTION_NAME, 'merchant_id')

    def get_downloader_path(self):
        path_setting = self.parser.get(self.DOWNLOADER_SECTION_NAME,
            'dest_path')
        return os.path.abspath(os.path.expandvars(path_setting))


if __name__ == '__main__':
    config = RdioConfig('config.ini')

    print "Rdio section:"
    print config.get_rdio_key()
    print config.get_rdio_secret()

    print "Rdio Downlaoder section:"
    print config.get_downloader_path()

    print "LinkShare section:"
    print config.get_linkshare_key()
    print config.get_linkshare_merchant_id()
