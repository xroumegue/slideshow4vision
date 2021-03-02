#! /usr/bin/env python3

import logging
import argparse
import wget
from pyunsplash import PyUnsplash
from os import system, mkdir, getcwd
from os.path import join, exists
from datetime import datetime

API_KEY_FILE=".api_key"
MAX_PER_PAGE=30

key_required=True

if exists(API_KEY_FILE):
    key_required=False

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--api-key", help="Developer API key", required=key_required)
parser.add_argument("-n", "--count", help="Number of photos to grab", type=int, default=32)
parser.add_argument("-q", "--query", help="Keywords to add on query", nargs='+', default=["white,cat"])
parser.add_argument("-W", "--width", help="Picture width", type=int, default=720)
parser.add_argument("-H", "--height", help="Picture height", type=int, default=576)
parser.add_argument("-d", "--download-only", help="Only download pictures", action='store_true')
parser.add_argument("-v", "--verbose", help="Verbose log in file", action='store_const', const=logging.DEBUG, default=logging.INFO)
parser.add_argument("-o", "--output", help="Slideshow output file", default='slideshow.mkv')
args = parser.parse_args()


if args.api_key:
    with open(API_KEY_FILE, 'w') as f:
        f.write(args.api_key)
    api_key=args.api_key
else:
    with open(API_KEY_FILE, 'r') as f:
        api_key = f.read()

# Initialize app logging
logger = logging.getLogger()
logging.basicConfig(filename='app.log',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=args.verbose,
        datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger(PyUnsplash.logger_name).setLevel(args.verbose)


# instantiate PyUnsplash object
py_un = PyUnsplash(api_key=api_key)

now = datetime.now().strftime("slideshow-%d_%m_%Y-%H:%M:%S")
outDir = join(getcwd(), now)
mkdir(outDir)

if args.count > MAX_PER_PAGE:
    pages = (args.count  + (MAX_PER_PAGE - 1)) // MAX_PER_PAGE
    per_page = MAX_PER_PAGE
else:
    pages = 1
    per_page = args.count

for q in args.query:
    count = 0
    print("Collecting {:s} query".format(q))
    search = py_un.search(type_='photos', page=pages, per_page=per_page, query=str(q))
    while search and search.has_next:
        #print(collections_page)
        for photo in search.entries:
            urls = photo.body.get('urls', None)['raw']
            url="{:s}&fit=crop&crop=focalpoint&w={:d}&h={:d}&fm=jpg".format(urls, args.width, args.height)
            outFile=join(outDir, '{:s}-{:d}x{:d}.jpg'.format(photo.id, args.width, args.height))
            wget.download(url, out=outFile)
            count = count + 1
            if (count >= args.count):
                search = None
                break
        if (search):
            search = search.get_next_page()
            search.url = 'photos'
        print("\nCount: {}/{}\n".format(count, args.count))

if not args.download_only:
    print("\nGenerating {:s}\n".format(args.output))
    inFiles=join(outDir, '*.jpg')
    outFile=join(outDir, args.output)
    ffmpeg_cmd="ffmpeg -y -r 1/3 -pattern_type glob -i \'{:s}\' -vf fps=fps=5 -c:v libx264 -preset slow -tune stillimage {:s}".format(inFiles, outFile)
    system(ffmpeg_cmd)
