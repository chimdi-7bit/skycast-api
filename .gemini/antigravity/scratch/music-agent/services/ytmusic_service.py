from ytmusicapi import YTMusic # import YTMusic from ytmusicapi
# 
class YTMusicService: # define YTMusicService class
    def __init__(self, auth_header_or_file): # define initialization method
        # ytmusicapi can take either a JSON string, a path to a JSON file, or an OAuth response. # comment
        # This implementation assumes the user has already set up their auth file. # comment
        self.ytm = YTMusic(auth_header_or_file) # initialize YTMusic client
# 
    def create_playlist(self, name, description, tracks): # define method to create playlist
        video_ids = [] # initialize empty list for video IDs
        for track in tracks: # iterate through each provided track
            search_query = f"{track['name']} {track['artist']}" # formulate search query
            if track.get('isrc'): # check if track has an ISRC
                # Prioritize ISRC search # comment
                search_results = self.ytm.search(track['isrc'], filter="songs") # search by ISRC
                if search_results: # if search returned results
                    video_ids.append(search_results[0]['videoId']) # append the topmost video ID
                    continue # skip to next track
# 
            # Fallback to name/artist search # comment
            search_results = self.ytm.search(search_query, filter="songs") # search by name and artist
            if search_results: # if search returned results
                video_ids.append(search_results[0]['videoId']) # append the topmost video ID
# 
        playlist_id = self.ytm.create_playlist(name, description, video_ids=video_ids) # create playlist on YTM with gathered video IDs
        return playlist_id # return the new playlist's ID
