from spotipy import util

import sys
import spotipy
import spotipy.util as util

import json

import time

scope = 'user-library-read'


def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0], ))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if not token:
        print("Can't get token for", username)

    sp = spotipy.Spotify(auth=token)

    album_store = AlbumStore()

    results = sp.current_user_saved_albums()

    num_albums = 0

    while True:
        for item in results['items']:
            album = item['album']
            album['added_at'] = item['added_at']

            album_store.add(album)
            num_albums += 1

        if not results['next']:
            break

        print("%s albums fetched..." % num_albums)

        # be extra nice to our hugops friends at Spotify
        time.sleep(1)
        results = sp.next(results)

    album_store.write_albums()
    print("done")


class AlbumStore(object):
    albumstore_filename = 'albums.json'

    def __init__(self):
        self.albums = {}

        with open(self.albumstore_filename, 'w+') as f:
            self.albums = json.loads(f.read() or "{}")

    def add(self, album):
        # skip these large and unused fields
        album['available_markets'] = None
        album['tracks'] = None

        self.albums[album['id']] = album

    def write_albums(self):
        with open(self.albumstore_filename, 'w') as f:
            f.write(json.dumps(self.albums))


main()
