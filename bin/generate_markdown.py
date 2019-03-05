import dateutil.parser as dp
import json


class AlbumFormatter(object):
    def __init__(self, album):
        self.album = album

    def _raw_album_url(self):
        return self.album['external_urls']['spotify']

    def image(self):
        image = None
        for i in self.album['images']:
            if not image:
                image = i

            if i['height'] == 64 or (image['height'] < 300 and i['height'] > image['height']):
                image = i

        if not image:
            return "None"

        image = '<a href="%s" target="_blank"><img width="64" src="%s"></a>' % (
            self._raw_album_url(), image['url'])

        return image

    def name(self):
        return '<a href="%s" target="_blank">%s</a>' % (self._raw_album_url(),
                                                        self.album['name'])

    def artists(self):
        return "<br>".join(
            map(
                lambda a: '<a href="%s" target="_blank">%s</a>' % (a[
                    'external_urls']['spotify'], a['name']),
                self.album['artists']))

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
        with open(self.recent_albums_filename, 'w') as f:
            f.write("# Recent Albums\n\n")
            f.write(
                "Cover|Album|Artist|Release Date|Tracks|Library Add Date\n")
            f.write(
                "-----|-----|------|------------|------|----------------\n")

            for album in self._get_recent_albums():
                afmt = AlbumFormatter(album)
                doc = "%s | %s | %s | %s | %s | %s\n" % (
                    afmt.image(), afmt.name(), afmt.artists(),
                    afmt.release_date(), afmt.total_tracks(),
                    afmt.library_add_date())

                f.write(doc)


MarkdownGenerator().write_recent_albums()
