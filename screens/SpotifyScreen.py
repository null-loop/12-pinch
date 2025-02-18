import json
import math
import os
import urllib

import mahotas
import spotipy
from PIL import Image
from spotipy.oauth2 import SpotifyOAuth

from screens.ImageScreenBase import ImageScreenBase
from utils.matrix import ScreenMatrix

class SpotifyScreen(ImageScreenBase):
    update_interval_seconds=5
    label="Spotify"

    def __init__(self, matrix: ScreenMatrix):
        super().__init__(matrix)
        self.__local_image_cache_dir = '.local-image-cache'

        if not os.path.isdir(self.__local_image_cache_dir):
            os.mkdir(self.__local_image_cache_dir)

        with open('./secrets/.spotify-secrets', 'r') as secrets_file:
            secrets = json.load(secrets_file)

        with open('./config/deny-artists.json', 'r') as deny_artists_file:
            self.__deny_artists = json.load(deny_artists_file)

        auth_manager = SpotifyOAuth(client_id=secrets['client-id'], client_secret=secrets['client-secret'],
                                    scope='user-read-playback-state',
                                    redirect_uri='http://localhost:8080/spotify/callback')
        self.__spotify = spotipy.Spotify(auth_manager=auth_manager)
        self.__last_image_url = ""

    def render(self) -> Image:
        try:
            current = self.__spotify.current_user_playing_track()
            if current is not None:
                current_album = current['item']['album']
                artists = current['item']['artists']
                # if any artist name is in the deny_artists list we don't update
                denied = False
                for artist in artists:
                    if artist['name'].lower() in self.__deny_artists:
                        denied = True

                if denied:
                    current_image_url = self.__last_image_url
                else:
                    current_image_url = current_album['images'][0]['url']

                self.__last_image_url = current_image_url

            if self.__last_image_url:
                image_id = urllib.parse.urlparse(self.__last_image_url).path.split('/')[-1]
                cached_image_path = self.__local_image_cache_dir +'/' + image_id + '.png'

                if not os.path.isfile(cached_image_path):
                    urllib.request.urlretrieve(self.__last_image_url, 'temp-download.jpg')
                    jpg = mahotas.imread('temp-download.jpg')
                    mahotas.imsave(cached_image_path, jpg)
                    image = Image.open(cached_image_path)
                    image.thumbnail((128, 128))
                    image.save(cached_image_path)
                else:
                    image = Image.open(cached_image_path)

                return image
        except:
            print("Error updating image.")