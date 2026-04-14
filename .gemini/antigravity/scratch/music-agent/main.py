import os # import os module for environment variables
from services.spotify_service import SpotifyService # import SpotifyService class
from services.ytmusic_service import YTMusicService # import YTMusicService class
from utils.matcher import TrackMatcher # import TrackMatcher class
# 
def transfer_spotify_to_ytm(spotify_playlist_id, spotify_creds, ytm_auth): # define main transfer function
    # Initialize services # comment
    spotify = SpotifyService( # instantiate SpotifyService
        client_id=spotify_creds['client_id'], # pass client_id
        client_secret=spotify_creds['client_secret'], # pass client_secret
        redirect_uri=spotify_creds['redirect_uri'] # pass redirect_uri
    ) # close instantiation
    ytm = YTMusicService(ytm_auth) # instantiate YTMusicService
    matcher = TrackMatcher() # instantiate TrackMatcher
# 
    # Step 1: Extract tracks from Spotify # comment
    print(f"Fetching tracks from Spotify playlist: {spotify_playlist_id}") # print status
    spotify_tracks = spotify.get_playlist_tracks(spotify_playlist_id) # fetch tracks
    print(f"Extracted {len(spotify_tracks)} tracks.") # print count of extracted tracks
# 
    # Step 2: Transfer (Reconstruct) on YouTube Music # comment
    print(f"Transferring to YouTube Music...") # print status
    playlist_id = ytm.create_playlist( # call create_playlist on YTM
        name="Transferred from Spotify", # set new playlist name
        description="A playlist transferred using my music-agent.", # set playlist description
        tracks=spotify_tracks # pass extracted spotify tracks
    ) # close method call
    print(f"Success! New playlist created on YouTube Music: {playlist_id}") # print success message
# 
if __name__ == "__main__": # check if script is run directly
    # Example placeholder for running the script. # comment
    # Replace these with real credentials. # comment
    SPOTIFY_CREDS = { # define spotify credentials dictionary
        'client_id': os.environ.get('SPOTIFY_CLIENT_ID', 'YOUR_SPOTIFY_CLIENT_ID'), # get client id from env or use placeholder
        'client_secret': os.environ.get('SPOTIFY_CLIENT_SECRET', 'YOUR_SPOTIFY_CLIENT_SECRET'), # get secret from env or use placeholder
        'redirect_uri': 'http://localhost:8888/callback' # set redirect uri
    } # close dictionary
# 
    YTM_AUTH = 'oauth.json' # specify YTM auth file path
# 
    SPOTIFY_PLAYLIST_ID = os.environ.get('SPOTIFY_PLAYLIST_ID', 'YOUR_PLAYLIST_ID') # get playlist ID from env or use placeholder
# 
    # To run this, you'd call: # comment
    if SPOTIFY_PLAYLIST_ID != 'YOUR_PLAYLIST_ID': # check if playlist ID is set
        transfer_spotify_to_ytm(SPOTIFY_PLAYLIST_ID, SPOTIFY_CREDS, YTM_AUTH) # execute transfer
    else: # if not set
        print("Please set the SPOTIFY_PLAYLIST_ID environment variable to run.") # print warning
