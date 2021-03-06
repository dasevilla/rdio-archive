import codecs
import json
from datetime import date
import os

from rdiohelper import RdioHelper, RdioOptions
from rdioconfig import RdioConfig


class RdioCaller:

    ITEMS_PER_REQUEST = 500

    def __init__(self, config):
        self.config = config
        options = RdioOptions(self.config.get_rdio_key(),
                self.config.get_rdio_secret())
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
        result_size = 0
        while True:
            storage.extend(result)

            start += result_size
            args['start'] = start
            args['count'] = self.ITEMS_PER_REQUEST
            result = rdio_fn(**args)
            result_size = len(result)
            if result_size <= 0:
                break

        return storage

    def save_result(self, filename, storage):
        fp = codecs.open(filename, 'w', encoding='utf-8')
        json.dump(storage, fp, sort_keys=True, indent=4)


def get_new_releases():
    config = RdioConfig('config.ini')
    rdio_caller = RdioCaller(config)
    time_frames = ['thisweek', 'lastweek', 'twoweeks']
    for time_frame in time_frames:
        new_releases = rdio_caller.get_new_releases(time_frame)

        today = date.today()
        weeknumber = today.isocalendar()[1]
        if today.weekday() == 0:
            weeknumber -= 1

        if time_frame == 'lastweek':
            weeknumber -= 1
        elif time_frame == 'twoweeks':
            weeknumber -= 2

        year_number = today.isocalendar()[0]

        dest_dir = config.get_downloader_path()
        year_dir = os.path.join(dest_dir, str(year_number))

        if not os.path.exists(year_dir):
            os.makedirs(year_dir)

        file_name = 'music-%02d.json' % weeknumber
        abs_path = os.path.join(year_dir, file_name)
        rdio_caller.save_result(abs_path, new_releases)


if __name__ == "__main__":
    get_new_releases()
