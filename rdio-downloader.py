import codecs
import json
from datetime import date

from rdiohelper import RdioHelper, RdioOptions

import rdioconfig


class RdioCaller:

    ITEMS_PER_REQUEST = 500

    def __init__(self):
        options = RdioOptions(rdioconfig.CONSUMER_KEY,
                rdioconfig.CONSUMER_SECRET)
        self.rdio_helper = RdioHelper(options)

    def get_collection(self, user):
        return self.make_call(self.rdio_helper.getArtistsInCollection,
                user=user)

    def get_new_releases(self, time_frame='thisweek'):
        return self.make_call(self.rdio_helper.getNewReleases, time=time_frame)

    def make_call(self, rdio_fn, **args):
        storage = []
        start = 0
        result = []
        result_size = 1
        while result_size > 0:
            storage.extend(result)

            start += result_size
            args['start'] = start
            args['count'] = self.ITEMS_PER_REQUEST
            result = rdio_fn(**args)
            result_size = len(result)

        return storage

    def save_result(self, filename, storage):
        fp = codecs.open(filename, 'w', encoding='utf-8')
        json.dump(storage, fp, sort_keys=True, indent=4)


def get_new_releases():
    rdio_caller = RdioCaller()
    time_frames = ['thisweek', 'lastweek', 'twoweeks']
    for time_frame in time_frames:
        new_releases = rdio_caller.get_new_releases(time_frame)

        weeknumber = date.today().isocalendar()[1]

        if time_frame == 'lastweek':
            weeknumber -= 1
        elif time_frame == 'twoweeks':
            weeknumber -= 2

        filename = 'data/music-%02d.json' % weeknumber
        rdio_caller.save_result(filename, new_releases)


if __name__ == "__main__":
    get_new_releases()
