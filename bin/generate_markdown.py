import dateutil.parser as dp
import json


class AlbumFormatter(object):
    def __init__(self, album):
        self.album = album

    def image(self):
        image_url = next(img for img in self.album['images']
                         if img['height'] == 300)['url']

        url = self.album['external_urls']['spotify']

        image = '<a href="%s" target="_blank"><img width="100" src="%s"></a>' % (
            url, image_url)

        return image

    def name(self):
        return self.album['name']

    def artists(self):
        return ",".join(
            map(lambda artist: artist['name'], self.album['artists']))

    def release_date(self):
        return self.album['release_date']

    def total_tracks(self):
        return self.album['total_tracks']

    def library_add_date(self):
        return dp.parse(self.album['added_at']).strftime('%F')


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
            f.write(
                "Cover|Album|Artist|Release Date|Tracks|Library Add Date\n")
            f.write(
                "-----|-----|------|------------|------|----------------\n")

            for album in self._get_recent_albums():
                # ignore for pprint-ing
                album['available_markets'] = None
                album['tracks'] = None

                afmt = AlbumFormatter(album)
                doc = "%s | %s | %s | %s | %s | %s" % (
                    afmt.image(), afmt.name(), afmt.artists(),
                    afmt.release_date(), afmt.total_tracks(),
                    afmt.library_add_date())

                f.write(doc)


MarkdownGenerator().write_recent_albums()
