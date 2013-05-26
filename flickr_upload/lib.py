from __future__ import absolute_import
import logging
import os

import flickr_api as Flickr
from flickr_api import set_auth_handler
from flickr_api.auth import AuthHandler

AUTH_FILE = "~/.flickr_upload.auth"
"""saved authentication credentials"""


def init(key, secret):
    """
    Initialize API.

    @see: http://www.flickr.com/services/api/

    @param key: str, API key
    @param secret: str, API secret
    """
    # TODO: save keys in file too, and share with download tool
    logging.debug('Initializing Flickr API ({0}/{1})'.format(key, secret))
    Flickr.set_keys(key, secret)

    auth_file = os.path.expanduser(AUTH_FILE)
    logging.debug('Loading credentials from: {0}'.format(auth_file))
    try:
        handler = AuthHandler.load(auth_file)
        set_auth_handler(handler)
        return
    except IOError:
        logging.warning('Could not load credentials from: {0}'.format(auth_file))
        # fall through and create the file
        pass

    # Get new crendentials
    logging.debug('Retrieving new credentials from Flickr')
    handler = AuthHandler(key=key, secret=secret)
    print('Please authorize: {0}'.format(handler.get_authorization_url('write')))
    # TODO: make landing page that extracts the verifier
    verifier = raw_input('Verifier: ')
    handler.set_verifier(verifier)
    try:
        handler.save(auth_file)
    except IOError:
        logging.warning('Could not save credentials to: {0}'.format(auth_file))
    set_auth_handler(handler)


def add_common_options(parser):
    """
    TODO: dox
    """
    parser.add_argument('-k', '--api_key', type=str, required=True,
                        help='Flickr API key')
    parser.add_argument('-s', '--api_secret', type=str,
                        help='Flickr API secret')
    parser.add_argument('-d', '--debug', default=False, action='store_true',
                        help='turn on debugging')


def upload_photos(files):
    """
    Upload a list of files

    @param files: iterable, (file name, title, description)
    return: list(Flickr.Photo),
    """
    # TODO: add support for private/public
    ret = []
    for entry in files:
        (file_name, title) = entry
        logging.debug('Uploading: {0}'.format(file_name))
        photo = Flickr.Upload.upload(photo_file=file_name,
                                     is_public=0,
                                     title=title)
        ret.append(photo)
        logging.info('Uploaded photo to: {0}'.format(photo.getPageUrl()))
    return ret


def create_set(photos, title, description=None):
    logging.debug('Creating set: {0}'.format(title))
    photoset = Flickr.Photoset.create(primary_photo=photos[0], title=title,
                                      description=description)
    for photo in photos[1:]:
        photoset.addPhoto(photo_id=photo.id)
    # TODO: find/implement .getPageUrl?
    return photoset
