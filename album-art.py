#!/usr/bin/env python
import time, sys, json, os
import spotipy
import urllib.request
from spotipy.oauth2 import SpotifyOAuth
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

print(os.path.dirname(__file__))

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)

with open('.spotify-secrets', 'r') as secrets_file:
    secrets = json.load(secrets_file)

auth_manager = SpotifyOAuth(client_id=secrets['client-id'], client_secret=secrets['client-secret'], scope='user-read-playback-state', redirect_uri='http://localhost:8080/spotify/callback')
sp = spotipy.Spotify(auth_manager=auth_manager)

last_image_url = ""
image_file_name = os.path.join(os.path.dirname(__file__), 'current_image.jpg')

try:
    print("Press CTRL-C to stop.")
    while True:
        current = sp.current_user_playing_track()
        current_album = current['item']['album']
        current_image_url = current_album['images'][0]['url']
        if current_image_url != last_image_url:
            urllib.request.urlretrieve(current_image_url, image_file_name)
            last_image_url = current_image_url
            print("Updating image to " + current_album['name'])
            image = Image.open(image_file_name)
            image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
            matrix.SetImage(image.convert('RGB'))
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit(0)