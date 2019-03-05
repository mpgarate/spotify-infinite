import dateutil.parser as dp
import json


class MarkdownGenerator(object):
    albumstore_filename = 'albums.json'
    recent_albums_filename = 'recent_albums.md'

    def __init__(self):
        self.albums = []

        with open(self.albumstore_filename, 'r') as f:
            self.albums = [v for k, v in json.loads(f.read() or "{}").items()]

    def _get_recent_albums(self):
        return sorted(
            self.albums,
            key=lambda a: dp.parse(a['added_at']).strftime('%s'),
            reverse=True)

    def write_recent_albums(self):
        from pprint import pprint

        with open(self.recent_albums_filename, 'w') as f:
            f.write("# Recent Albums\n\n")
            f.write("Cover|Album|Artist|Release Date|Tracks|Library Add Date\n")
            f.write("-----|-----|------|------------|------|----------------\n")

            for album in self._get_recent_albums():
                album['available_markets'] = None
                album['tracks'] = None

                # <img width="100" src="https://i.scdn.co/image/3768eb4a008c18600bcf8af2c2eed84124b55ab2"> | Beats, Not Words | Sol Monk | 2015 | 7 tracks | 123

                artists = ",".join(
                    map(lambda artist: artist['name'], album['artists']))

                image_url = next(img for img in album['images']
                                 if img['height'] == 300)['url']
                url = album['external_urls']['spotify']

                image = '<a href="%s" target="_blank"><img width="100" src="%s"></a>' % (
                    url, image_url)

                library_add_date = dp.parse(album['added_at']).strftime('%F')

                doc = "%s | %s | %s | %s | %s | %s" % (
                    image, album['name'], artists, album['release_date'],
                    album['total_tracks'], library_add_date)

                doc += "\n"

                f.write(doc)


MarkdownGenerator().write_recent_albums()
