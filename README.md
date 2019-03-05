# spotify-infinite

Scripts to download albums from Spotify and add to an append-only local store.

This helps remember more albums than can be saved under the current spotify 10k track limit.

A caveat of this approach is that all albums removed from the Spotify library will remain here once added. If desired, those can be deleted from the json blob manually.

## Local setup
On Ubuntu:

```sh
./setup.sh
```

Set environment variables
```
export SPOTIPY_CLIENT_ID='123'
export SPOTIPY_CLIENT_SECRET='123'

# does not need to really answer the redirect
export SPOTIPY_REDIRECT_URI='http://localhost/foo/bar'
```

## Usage

### Get albums

On first run, this will show a URL to open and sign in with your Spotify account. This token is cached locally for future runs.

```sh
USERNAME=your-spotify-username
python3 bin/get_albums.py $USERNAME
```

### Generate Markdown
```sh
python bin/generate_markdown.py
```
