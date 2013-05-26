from __future__ import absolute_import
import argparse
from collections import OrderedDict
import logging
import sys

from phpserialize import load
from phpserialize import phpobject

from lib import add_common_options
from lib import create_set
from lib import init
from lib import upload_photos


class Album(object):
    def __init__(self, fields, **kwargs):
        self.title = fields['title']
        self.description = fields['description']


class AlbumItem(object):
    def __init__(self, caption, image, **kwargs):
        # TODO upload/capture date?
        self.caption = caption
        self.image = image

    def __repr__(self):
        return "{0}: {1}".format(self.image, self.caption)


class Image(object):
    def __init__(self, name, type, **kwargs):
        self.filename = "{0}.{1}".format(name, type)

    def __repr__(self):
        return self.filename


def object_hook(class_name, data):
    reg = {'Album': Album, 'AlbumItem': AlbumItem, 'Image': Image}
    clazz = reg.get(class_name)
    if not clazz:
        return phpobject(class_name, data)

    return clazz(**data)


def file_generator(photos):
    """
    Generator that generates photo data

    @param photos: OrderedDict, Gallery photo data
    @return: (file name, caption) generator
    """
    for num in photos:
        item = photos[num]
        yield (item.image.filename, item.caption)


def read_dat(fname):
    """
    Read PHP serialized .dat file

    @param fname: str, filename
    @return: object structure
    """
    logging.debug('Reading data from: {0}'.format(fname))
    with open(fname, "r") as fh:
        data = load(fh,
                    array_hook=OrderedDict,
                    object_hook=object_hook)
    return data


def main():
    parser = argparse.ArgumentParser('Upload photos to Flickr')
    add_common_options(parser)

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    init(args.api_key, args.api_secret)

    album = read_dat('album.dat')
    photo_data = read_dat('photos.dat')
    logging.debug('Will upload {0} photos to set: {1}'.format(len(photo_data),
                                                              album.title))
    photos = upload_photos(file_generator(photo_data))
    photoset = create_set(photos, title=album.title, description=album.description)


if __name__ == "__main__":
    sys.exit(main())
