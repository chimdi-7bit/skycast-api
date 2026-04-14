from rapidfuzz import fuzz # import fuzz module from rapidfuzz
# 
class TrackMatcher: # define TrackMatcher class
    def __init__(self, threshold=85): # define initialization method with default threshold
        self.threshold = threshold # assign threshold to instance
# 
    def is_match(self, source_track, candidate_track): # define method to check if two tracks match
        # 1. Primary Match: ISRC (The Gold Standard) # comment
        source_isrc = source_track.get('isrc') # get source ISRC
        candidate_isrc = candidate_track.get('isrc') # get candidate ISRC
        if source_isrc and candidate_isrc and source_isrc == candidate_isrc: # check if both have ISRC and they are equal
            return True # return True for exact ISRC match
# 
        # 2. Secondary Match: Fuzzy Title + Artist # comment
        source_str = f"{source_track['artist']} {source_track['name']}".lower() # format source string for comparison
        candidate_str = f"{candidate_track['artist']} {candidate_track['name']}".lower() # format candidate string for comparison
# 
        similarity = fuzz.token_sort_ratio(source_str, candidate_str) # calculate string similarity score
        if similarity >= self.threshold: # check if similarity meets threshold
            # Check duration similarity (within 5 seconds) # comment
            if 'duration_ms' in source_track and 'duration_ms' in candidate_track: # verify both have duration
                duration_diff = abs(source_track['duration_ms'] - candidate_track['duration_ms']) # calculate duration difference
                if duration_diff <= 5000: # check if difference is 5 seconds or less
                    return True # return True as match is within bounds
        return False # return False if no match found
# 
    def find_best_match(self, source_track, candidate_tracks): # define method to find best match in a list
        best_match = None # initialize best_match as None
        highest_score = 0 # initialize highest_score as 0
# 
        for candidate in candidate_tracks: # iterate through each candidate track
            source_str = f"{source_track['artist']} {source_track['name']}".lower() # format source string
            candidate_str = f"{candidate['artist']} {candidate['name']}".lower() # format candidate string
            score = fuzz.token_sort_ratio(source_str, candidate_str) # calculate similarity score
# 
            if score > highest_score and score >= self.threshold: # check if score is highest and above threshold
                highest_score = score # update highest score
                best_match = candidate # update best match
        return best_match # return the matching track
