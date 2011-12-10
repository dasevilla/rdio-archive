import codecs
import json
import os
import os.path
import re
from datetime import date, timedelta
import errno
import glob

import pystache

from rdioconfig import RdioConfig
import linkshare


class Week(object):
    FILE_NAME_PATTERN = 'music-(\d\d).json$'
    PAGE_SIZE = 40

    def __init__(self, filename, linkshare_helper):
        self.filename = filename
        self.linkshare_helper = linkshare_helper
        self.week_number = self.get_week_number(filename)

    def get_path(self):
        return "%s" % self.week_number

    def get_first_page_path(self):
        return "%s/week-%02d-page-%02d.html" % (self.get_path(),
            self.week_number, 1)

    def get_albums(self, filename):
        with codecs.open(filename, 'r', encoding='utf-8') as fp:
            return json.load(fp)

    def get_week_number(self, filename):
        matches = re.search(self.FILE_NAME_PATTERN, filename)
        return int(matches.group(1))

    def pre_process_albums(self, albums):
        for album in albums:
            album_url = 'http://www.rdio.com%s' % album['url']
            album['url'] = self.linkshare_helper.generate_link_simple(
                album_url)

            artist_url = 'http://www.rdio.com%s' % album['artistUrl']
            album['artistUrl'] = self.linkshare_helper.generate_link_simple(
                artist_url)

    def paginate(self):
        albums = self.get_albums(self.filename)
        self.pre_process_albums(albums)

        first_page = None
        prev_page = None
        page_number = 1

        for page_start in range(0, len(albums), self.PAGE_SIZE):
            album_subset = albums[page_start:page_start + self.PAGE_SIZE]

            curr_page = Page(prev_page, None, album_subset, page_number, self)

            if not first_page:
                first_page = curr_page

            if prev_page:
                prev_page.next_page = curr_page

            prev_page = curr_page
            page_number += 1

        return first_page


class Page(object):

    def __init__(self, prev_page, next_page, albums, page_number, week):
        self.prev_page = prev_page
        self.next_page = next_page
        self.albums = albums
        self.page_number = page_number
        self.week = week
        self.filename = "week-%02d-page-%02d.html" % (week.week_number,
            page_number)

    def get_path(self):
        return "%s/%s" % (self.week.get_path(), self.filename)


class WeekLoader(object):

    FILE_NAME_GLOB = 'music-*.json'

    def __init__(self, config):
        self.config = config
        linkshare_helper = linkshare.LinkShareHelper(
            self.config.get_linkshare_key(),
            self.config.get_linkshare_merchant_id())
        self.week_list = []
        for src_filename in self.get_src_filenames():
            self.week_list.append(Week(src_filename, linkshare_helper))

    def get_src_filenames(self):
        glob_pattern = os.path.join(self.config.get_downloader_path(),
            self.FILE_NAME_GLOB)
        src_filenames = glob.glob(glob_pattern)
        return src_filenames


class HtmlGenerator(object):

    TEMPLATE_NAME = 'template/archive-page.mustache'

    def __init__(self, week_list, config):
        self.config = config
        self.week_list = week_list

        with codecs.open(self.TEMPLATE_NAME, 'r', encoding='utf-8') as fp:
            self.template = fp.read()

    def generate_toc(self, current_week):
        toc = []
        for week in self.week_list:
            toc.append({
                'weekNumber': week.week_number,
                'path': week.get_first_page_path(),
                'currentWeek': current_week is week,
            })

        return toc

    def generate_pagination(self, page):
        if page.next_page:
            next_link = page.next_page.filename
        else:
            next_link = None

        if page.prev_page:
            prev_link = page.prev_page.filename
        else:
            prev_link = None

        pagination = {
            'nextLink': next_link,
            'prevLink': prev_link,
        }

        return pagination

    def generate_all(self):
        for week in self.week_list:
            self.generate_week(week)

    def week_start_date(self, year, week):
        d = date(year, 1, 1)
        delta_days = d.isoweekday() - 1
        delta_weeks = week
        if year == d.isocalendar()[0]:
            delta_weeks -= 1
        delta = timedelta(days=-delta_days, weeks=delta_weeks)
        day_delta = timedelta(days=1)
        return d + delta + day_delta

    def generate_week(self, week):
        full_path = os.path.join(self.config.get_archiver_path(),
            week.get_path())
        try:
            os.mkdir(full_path)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise

        toc = self.generate_toc(week)
        page = week.paginate()
        while page:

            start_date = self.week_start_date(2011, week.week_number)

            template_vars = {
                'weekNumber': week.week_number,
                'pageNumber': page.page_number,
                'releaseDate': start_date.strftime("%B %d, %Y"),
                'pagination': self.generate_pagination(page),
                'albums': page.albums,
                'toc': toc,
            }

            rendered_template = pystache.render(self.template, template_vars)

            full_path = os.path.join(self.config.get_archiver_path(),
                page.get_path())
            with codecs.open(full_path, 'w', encoding='utf-8') as fp:
                fp.write(rendered_template)

            page = page.next_page


if __name__ == "__main__":
    config = RdioConfig('config.ini')
    loader = WeekLoader(config)
    sorted_week = sorted(loader.week_list, key=lambda week: week.week_number)
    generator = HtmlGenerator(sorted_week, config)
    generator.generate_all()
