#!/usr/bin/env python

# Copyright (c) 2020 Ryo Sakagami
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

"""
Utility functions for showing Spotify information on Vector's screen.
"""
import os
import time
from PIL import Image
import requests
from io import BytesIO

import anki_vector
import anki_vector.util
import spotipy
import spotipy.util

from config import CLIENT_ID, CLIENT_SECRET, USER, REDIRECT_URI

SCREEN_WIDTH = 184
SCREEN_HEIGHT = 96

SCOPE = 'user-read-currently-playing'

def init_spotify_client():
    token = spotipy.util.prompt_for_user_token(
        USER,
        scope=SCOPE,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI
    )
    spotify = spotipy.Spotify(auth=token)
    return spotify


def get_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def adjust_image_for_vector(img):
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    # create thumbnail that fits in Vector's monitor
    img.thumbnail(size=size)

    # calculate offset to place thumbnail in the center
    offset_x = max(int((size[0] - img.size[0]) / 2), 0)
    offset_y = max(int((size[1] - img.size[1]) / 2), 0)
    offset_tuple = (offset_x, offset_y)

    # create the image object to be the final product
    final_img = Image.new(mode='RGBA', size=size, color=(0, 0, 0, 0))

    # paste the thumbnail into the full sized image
    final_img.paste(img, offset_tuple)
    return final_img

def show_artwork(robot, artwork_url, duration_s=4.0):
    # Load an image
    artwork_file = get_image_from_url(artwork_url)
    artwork_file = adjust_image_for_vector(artwork_file)

    # Convert the image to the format used by the Screen
    print("Display artwork image on Vector's face...")
    screen_data = anki_vector.screen.convert_image_to_screen_data(artwork_file)

    robot.screen.set_screen_with_image_data(screen_data, duration_s)
    time.sleep(duration_s)

def show_current_track(robot, track):
    # show artwork
    artwork_url = track['item']['album']['images'][1]['url']
    show_artwork(robot, artwork_url)
    # show track



