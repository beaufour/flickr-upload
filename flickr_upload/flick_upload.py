#!/usr/bin/python
#
# Util to upload files to Flickr
#

from __future__ import absolute_import
import argparse
import logging
import os
import sys

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


def upload_photo(fname):
    """
    Uploads the given file to Flickr

    @param fname: str, path to file
    @return: flickr_api.Photo, uploaded photo object
    """
    # TODO: figure out params
    logging.debug('Uploading: {0}'.format(fname))
    photo = Flickr.Upload.upload(photo_file=fname, is_public=0)
    logging.debug('Uploaded: {0}'.format(photo))
    return photo


def main():
    parser = argparse.ArgumentParser('Download a Flickr Set')
    parser.add_argument('-k', '--api_key', type=str, required=True,
                        help='Flickr API key')
    parser.add_argument('-s', '--api_secret', type=str,
                        help='Flickr API secret')
    parser.add_argument('-d', '--debug', default=False, action='store_true',
                        help='turn on debugging')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    init(args.api_key, args.api_secret)
    photo = upload_photo('test.jpg')
    print('Uploaded photo to: {0}'.format(photo.getPageUrl()))


if __name__ == '__main__':
    sys.exit(main())
