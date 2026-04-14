import spotipy # import spotipy library
from spotipy.oauth2 import SpotifyOAuth # import SpotifyOAuth for authentication
# 
class SpotifyService: # define SpotifyService class
    def __init__(self, client_id, client_secret, redirect_uri): # define initialization method
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth( # initialize spotipy client with auth manager
            client_id=client_id, # pass client id
            client_secret=client_secret, # pass client secret
            redirect_uri=redirect_uri, # pass redirect uri
            scope="playlist-read-private" # set scope for reading private playlists
        )) # close auth manager and spotipy client instantiation
# 
    def get_playlist_tracks(self, playlist_id): # define method to get tracks
        results = self.sp.playlist_tracks(playlist_id) # fetch initial page of tracks
        tracks = results['items'] # extract items from results
        while results['next']: # iterate while there is a next page
            results = self.sp.next(results) # fetch next page
            tracks.extend(results['items']) # append tracks to list
# 
        extracted_tracks = [] # initialize empty list for extracted tracks
        for item in tracks: # iterate over each track item
            track = item['track'] # extract track object
            extracted_tracks.append({ # append dictionary containing track details
                'name': track['name'], # get track name
                'artist': track['artists'][0]['name'], # get first artist's name
                'album': track['album']['name'], # get album name
                'isrc': track.get('external_ids', {}).get('isrc'), # safely get ISRC if available
                'duration_ms': track['duration_ms'] # get duration in ms
            }) # close dictionary
        return extracted_tracks # return the final list
