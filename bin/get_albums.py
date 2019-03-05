from spotipy import util

import sys
import spotipy
import spotipy.util as util

import json

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

    # TODO: get more data
    results = sp.current_user_saved_albums()

    for item in results['items']:
        album = item['album']
        album['added_at'] = item['added_at']

        album_store.add(album)

    album_store.write_albums()


class AlbumStore(object):
    albumstore_filename = 'albums.json'

    def __init__(self):
        self.albums = {}

        with open(self.albumstore_filename, 'w+') as f:
            self.albums = json.loads(f.read() or "{}")

    def add(self, album):
        self.albums[album['id']] = album

    def write_albums(self):
        with open(self.albumstore_filename, 'w') as f:
            f.write(json.dumps(self.albums))


main()
