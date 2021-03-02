# slideshow4vision
Generate slideshow


# Getting started

git clone https://github.com/xroumegue/slideshow4vision.git

cd slideshow4vision

In case you want to isolate yourself from your distribution:
- python3 -m venv venv
- . venv/bin/activate

pip install -r requirements.txt

Install ffmpeg if required:
- apt install ffmpeg
- dnf install ffmpeg


You have to create a developer account on https://unsplash.com/documentation/#creating-a-developer-account,
to get an api key.

# Usage
```
usage: slideshow4vision.py [-h] -k API_KEY [-n COUNT] [-q QUERY [QUERY ...]] [-W WIDTH] [-H HEIGHT] [-d] [-v] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -k API_KEY, --api-key API_KEY
                        Developer API key
  -n COUNT, --count COUNT
                        Number of photos to grab
  -q QUERY [QUERY ...], --query QUERY [QUERY ...]
                        Keywords to add on query
  -W WIDTH, --width WIDTH
                        Picture width
  -H HEIGHT, --height HEIGHT
                        Picture height
  -d, --download-only   Only download pictures
  -v, --verbose         Verbose log in file
  -o OUTPUT, --output OUTPUT
                        Slideshow output file
```

The api key is stored in .api_key file, so you only need to set the option once.

# Examples

To generate a slideshow of 16 different 720x576 pictures of white dogs, black cats and horses:

./src/slideshow4vision.py -k <api_key> -W 720 -H 576 -n 16 -q 'white,dog' 'black,cat' 'horse' 'plane'
