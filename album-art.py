#!/usr/bin/env python
import time, sys, json, os
import spotipy
import mahotas
import urllib
from spotipy.oauth2 import SpotifyOAuth
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageFile


options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 4
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 2
options.limit_refresh_rate_hz = 120
options.brightness = 50
options.disable_hardware_pulsing = True
options.drop_privileges = False

matrix = RGBMatrix(options = options)

ImageFile.LOAD_TRUNCATED_IMAGES = True

local_image_cache_dir = '.local-image-cache'

#TODO:Purge cache arg

if not os.path.isdir(local_image_cache_dir):
    os.mkdir(local_image_cache_dir)

with open('.spotify-secrets', 'r') as secrets_file:
    secrets = json.load(secrets_file)

with open('deny-artists.json', 'r') as deny_artists_file:
    deny_artists = json.load(deny_artists_file)

auth_manager = SpotifyOAuth(client_id=secrets['client-id'], client_secret=secrets['client-secret'], scope='user-read-playback-state', redirect_uri='http://localhost:8080/spotify/callback')
sp = spotipy.Spotify(auth_manager=auth_manager)

last_image_url = ""

try:
    print("Press CTRL-C to stop.")
    while True:
        #TODO:Handle spotify / network time outs gracefully!
        try:
            current = sp.current_user_playing_track()
            if current is not None:
                current_album = current['item']['album']
                artists = current['item']['artists']
                # if any artist name is in the deny_artists list we don't update
                denied = False
                for artist in artists:
                    if artist['name'].lower() in deny_artists:
                        denied = True

                if denied:
                    continue

                current_image_url = current_album['images'][0]['url']
                if current_image_url != last_image_url:
                    print("Updating image to " + current_album['name'] + ' from ' + current_image_url)
                    last_image_url = current_image_url
                    image_id = urllib.parse.urlparse(current_image_url).path.split('/')[-1]
                    cached_image_path = local_image_cache_dir +'/' + image_id + '.png'

                    if not os.path.isfile(cached_image_path):
                        urllib.request.urlretrieve(current_image_url, 'temp-download.jpg')
                        jpg = mahotas.imread('temp-download.jpg')
                        mahotas.imsave(cached_image_path, jpg)
                        image = Image.open(cached_image_path)
                        image.thumbnail((128, 128))
                        image.save(cached_image_path)
                    else:
                        image = Image.open(cached_image_path)

                    top_half = image.crop((0,0,128,64))
                    bottom_half = image.crop((0,64,128,128))
                    bottom_half.save("current-bottom.png")

                    stitched = Image.new('RGB', (256, 64))
                    stitched.paste(top_half, (0, 0))
                    stitched.paste(bottom_half, (128, 0))

                    rgb = stitched.convert('RGB')

                    matrix.SetImage(rgb)
        except:
            print("Error updating image.")

        time.sleep(1)
except KeyboardInterrupt:
    sys.exit(0)