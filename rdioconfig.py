from ConfigParser import SafeConfigParser
import argparse
import codecs
import os


class RdioConfig:

    RDIO_SECTION_NAME = 'rdio'
    LINKSHARE_SECTION_NAME = 'linkshare'
    DOWNLOADER_SECTION_NAME = 'rdio-downloader'
    ARCHIVER_SECTION_NAME = 'rdio-archive'

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

    def get_archiver_path(self):
        path_setting = self.parser.get(self.ARCHIVER_SECTION_NAME,
            'dest_path')
        return os.path.abspath(os.path.expandvars(path_setting))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Rdio downloader options')
    parser.add_argument('value_name', action='store')
    results = parser.parse_args()

    config = RdioConfig('config.ini')

    config_func = getattr(config, results.value_name)
    print config_func()
