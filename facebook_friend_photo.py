#!/usr/bin/env python

import argparse
import json
import mimetypes
import os
import urllib
import urllib2
import urlparse

parser = argparse.ArgumentParser()
parser.add_argument('--access_token', required=True)
parser.add_argument('--owner_cursor_file')
parser.add_argument('--directory', required=True)
parser.add_argument('--size', type=int, default=160)

args = parser.parse_args()

q = 'SELECT id, url FROM square_profile_pic WHERE id IN (SELECT uid1 FROM friend WHERE uid2=me()) AND size=%d' % args.size

url = 'https://graph.prod.facebook.com/fql'

params = urllib.urlencode({
  'access_token': args.access_token,
  'q': q,
})

data = json.loads(urllib2.urlopen('%s?%s' % (url, params)).read())

for row in data['data']:
  image = urllib2.urlopen(row['url'])
  extension = mimetypes.guess_extension(image.headers.getheader('content-type'))
  filename = '%i%s' % (row['id'], extension)
  path = os.path.abspath('/'.join([args.directory, filename]))
  f = open(path, 'w')
  f.write(image.read())
  f.close()
