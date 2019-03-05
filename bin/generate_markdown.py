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
            self.albums, key=lambda a: dp.parse(a['added_at']).strftime('%s'), reverse=True)

    def write_recent_albums(self):
        from pprint import pprint

        with open(self.recent_albums_filename, 'w') as f:
            f.write("# Recent Albums\n\n")

            for album in self._get_recent_albums():
                album['available_markets'] = None
                album['tracks'] = None

                doc = "### %s\n" % album['name']

                artists = ",".join(map(lambda artist: artist['name'], album['artists']))
                doc += "#### %s\n" % artists

                image_url = next(img for img in album['images'] if img['height'] == 300)['url']
                url = album['external_urls']['spotify']
                doc += "[![%s](%s)](%s)\n" % (album['name'], image_url, url)

                doc += "Released %s\n" % album['release_date']

                doc += "%s tracks\n" % (album['total_tracks'])

                doc += "\n"

                f.write(doc)


MarkdownGenerator().write_recent_albums()
