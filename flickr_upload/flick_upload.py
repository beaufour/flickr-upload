#!/usr/bin/python
#
# Util to upload files to Flickr
#

from __future__ import absolute_import
import argparse
import csv
import glob
import logging
import os
import sys

import flickr_api as Flickr

from lib import add_common_options
from lib import create_set
from lib import init
from lib import upload_photos


def file_generator(files, descriptions=None):
    for entry in files:
        for fname in glob.glob(entry):
            yield (fname, descriptions.get(os.path.basename(fname)))


def load_description_file(fname):
    """
    Load and parse the photo descrition file.

    @param fname: str, path to file
    @return: dict, { 'set_name': str, 'photos': dict }
    """
    logging.info('Loading descriptions from: {0}'.format(fname))
    ret = {}
    with open(fname, 'rb') as csvfile:
        header = csvfile.readline().strip()
        ret['set_name'] = header
        reader = csv.reader(csvfile, delimiter=';')
        ret['photos'] = {}
        for row in reader:
            ret['photos'][row[0]] = row[1]

    return ret


def main():
    parser = argparse.ArgumentParser('Upload photos to Flickr')
    add_common_options(parser)
    parser.add_argument('-f', '--description_file', type=str,
                        help='optional description file with photo titles')
    parser.add_argument('file', nargs='+',
                        help='file(s) to upload')

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    init(args.api_key, args.api_secret)

    descr = None
    if args.description_file:
        descr = load_description_file(args.description_file)

    photos = upload_photos(file_generator(args.file, descr))

    set_name = descr.get('set_name')
    if set_name:
        create_set(photos, title=set_name)

if __name__ == '__main__':
    sys.exit(main())
