import codecs
import json
import os
import os.path
import re
from datetime import date, timedelta

import pystache


FILE_NAME_PATTERN = 'music-(\d\d).json$'


class Week(object):
    PAGE_SIZE = 40

    def __init__(self, filename):
        self.src_file = filename
        self.set_week_number()
        self.load_albums()

    def set_week_number(self):
        matches = re.search(FILE_NAME_PATTERN, self.src_file)
        self.week_number = int(matches.group(1))

    def load_albums(self):
        fp = codecs.open(self.src_file, 'r', encoding='utf-8')
        self.albums = json.load(fp)

    def get_path(self):
        return "%s" % self.week_number

    def paginate(self):
        first_page = None
        prev_page = None
        page_number = 1

        for page_start in range(0, len(self.albums), self.PAGE_SIZE):
            album_subset = self.albums[page_start:page_start + self.PAGE_SIZE]

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

    def __init__(self, src_dir):
        self.src_dir = src_dir
        self.week_list = []
        for src_filename in self.get_src_filenames():
            self.week_list.append(Week(src_filename))

    def get_src_filenames(self):

        def visit_dir(src_filenames, dirname, names):
            for name in names:
                subname = os.path.join(dirname, name)
                if os.path.isdir(subname):
                    continue
                elif re.search(FILE_NAME_PATTERN, name):
                    src_filenames.append(subname)

        src_filenames = []
        os.path.walk(self.src_dir, visit_dir, src_filenames)
        return src_filenames


class HtmlGenerator(object):

    TEMPLATE_NAME = 'template/archive-page.mustache'

    def __init__(self, week_list, dst_dir):
        self.week_list = week_list
        self.dst_dir = dst_dir

        fp = codecs.open(self.TEMPLATE_NAME, 'r', encoding='utf-8')
        self.template = fp.read()
        fp.close()

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
        # Make the week's directory
        os.mkdir("%s/%s" % (self.dst_dir, week.get_path()))

        page = week.paginate()
        while page:
            if page.next_page:
                next_link = page.next_page.filename
            else:
                next_link = None

            if page.prev_page:
                prev_link = page.prev_page.filename
            else:
                prev_link = None

            start_date = self.week_start_date(2011, week.week_number)

            template_vars = {
                'weekNumber': week.week_number,
                'pageNumber': page.page_number,
                'releaseDate': start_date.strftime("%B %d, %Y"),
                'albums': page.albums,
                'nextLink': next_link,
                'prevLink': prev_link,
                'weeks': [],
            }

            rendered_template = pystache.render(self.template, template_vars)

            page_path = "%s/%s" % (self.dst_dir, page.get_path())
            fp = codecs.open(page_path, 'w', encoding='utf-8')
            fp.write(rendered_template)
            fp.close()

            page = page.next_page


if __name__ == "__main__":
    loader = WeekLoader('data')
    generator = HtmlGenerator(loader.week_list, '_generated')
    generator.generate_all()
