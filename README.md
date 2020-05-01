# Vectify
Let's get your spotify information via Vector!

## Quick Setup
This package uses [spotipy](https://github.com/plamere/spotipy) for accessing the spotify information and [vector_text_stream](https://github.com/ryosakagami/vector_text_stream) for showing information on the Vector's screen.

- Create a Spotify app on https://developer.spotify.com/dashboard/
- In the Spotify app webpage,
    - Open 'Edit Settings.
    - Set http://localhost:8888/callback/ in 'Redirect URIs'.
    - Click 'Save'.
    - Copy 'Client ID' and 'Client Secret' for later use.
- Clone this repo
- `cd /path/to/this/repo`
- `cp vectify/_config_template.py vectify/config.py`
- Open the copied vectify/config.py with your favorit editor and
    - Replace 'CLIENT_ID' and 'CLIENT_SECRET' to your own ones.
    - Replace 'USER' to your user name of Spotify.
- `pip install .`
- `python initialize.py` and follow instructions. More precisely,
    - Authorize the app with your account on the webpage which is opened automatically.
    - Copy the redirected URL and paste into the terminal.
- Now, you should have a `/path/to/this/repo/.cache-username`. Open `/path/to/this/repo/vectify/config.py` again and assign the path to the cache file to CACHE_PATH.
- `pip install .` again so that the updated config.py is reinstalled.

## Run Example
- `cd /path/to/this/repo`
- `python examples/auto_track_checker.py`
- Now your Vector informs you of the track when Spotify plays the next one ;)

## How to Use
See [examples](https://github.com/ryosakagami/vectify/tree/master/examples)!

## Uninstall
`pip uninstall vectify`