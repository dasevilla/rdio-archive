import os
import json

from rdioapi import Rdio

import rdioconfig


class RdioHelper:

    RDIO_USER_CONFIG = '~/.rdio-tool.json'

    def __init__(self, options):

        # load the persistent state
        config_path = os.path.expanduser(self.RDIO_USER_CONFIG)
        if os.path.exists(config_path):
            self.config = json.load(file(config_path))
        else:
            self.config = {'auth_state': {}}

        # set up the keys
        if options.consumer_key is not None:
            self.config['consumer_key'] = options.consumer_key
        if options.consumer_secret is not None:
            self.config['consumer_secret'] = options.consumer_secret

        # create the Rdio client object
        self.client = Rdio(self.config['consumer_key'],
            self.config['consumer_secret'], self.config['auth_state'])

        if options.authenticate:
            import webbrowser
            webbrowser.open(self.client.begin_authentication('oob'))
            verifier = raw_input('Enter the PIN from the Rdio site: ').strip()
            self.client.complete_authentication(verifier)

        # save state
        with file(config_path, 'w') as f:
            json.dump(self.config, f, indent=True)
            f.write('\n')

    def authenticate(self):
        import webbrowser
        webbrowser.open(self.client.begin_authentication('oob'))
        verifier = raw_input('Enter the PIN from the Rdio site: ').strip()
        self.client.complete_authentication(verifier)

    def getObjectFromShortCode(self, short_code):
        return self.client.getObjectFromShortCode(short_code=short_code)

    def getObjectFromUrl(self, path):
        return self.client.getObjectFromUrl(url=path)

    def getNewReleases(self, **args):
        return self.client.getNewReleases(**args)

    def getArtistsInCollection(self, **args):
        return self.client.getArtistsInCollection(**args)


class RdioOptions:
    consumer_key = None
    consumer_secret = None
    authenticate = False

    def __init__(self, key, secret):
        self.consumer_key = key
        self.consumer_secret = secret


def main():
    from pprint import pprint

    options = RdioOptions(rdioconfig.CONSUMER_KEY, rdioconfig.CONSUMER_SECRET)
    # options.authenticate = True
    instance = RdioHelper(options)
    song = instance.getObjectFromShortCode('QE9MK29_fA')
    pprint(song)


if __name__ == "__main__":
    main()
