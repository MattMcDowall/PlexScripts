# For details on this script, see the README.md file in this repo

from plexapi.myplex import MyPlexAccount

print('Connecting to server . . .')
account = MyPlexAccount()   # Credentials retrieved from PlexAPI config.ini file
print('    . . . connection established.')
plex = account.resource('MEDIA').connect()

for collxn_title in ["Compilations", "Anthologies"]:
    for collxn in plex.library.section('Music').search(filters={"title==": collxn_title}, libtype="collection"):
        for album in collxn.items():
            print(album.parentTitle, '|', album.title, sep=' ')
            for comp_track in album.tracks():
                comp_rating = comp_track.userRating
                # - To speed things up, also limit to *rated* tracks
                # - Seems to crash if the track title begins with an apostrophe, so skip those
                # - Skip any that are already marked as dupes
                if ((comp_rating is not None) & (not comp_track.title.startswith("'")) & (all(m.tag != "Dupe" for m in comp_track.moods))):
                    # Search for:
                    #   *exact* title match AND
                    #   *non-matching* id (ratingKey) AND
                    #   matching track isn't marked as a Dupe
                    for album_track in plex.library.section('Music').search(filters={"title==": comp_track.title, "track.id!=": comp_track.ratingKey, "track.mood!=": "Dupe"}, libtype='track'):
                        # Check the difference in lengths
                        # Looking for an arbitrary threshold of <8 seconds difference
                        if(abs(album_track.duration - comp_track.duration) < 8000):
                            # Can't filter for artist name, so double-check it
                            #   "originalTitle" is the track artist
                            #   "grandparentTitle" is the album artist, which we check on
                            #       the album track in case the originalTitle isn't set (it
                            #       often isn't, if it's the same as the album artist for
                            #       all tracks).
                            if (album_track.originalTitle == comp_track.originalTitle) or (album_track.grandparentTitle == comp_track.originalTitle):
                                print('  ', comp_track.ratingKey, comp_track.originalTitle, comp_track.title, sep="\t")
                                print("\t\tDupe of:", album_track.ratingKey, album_track.title, '[' + album_track.parentTitle + ']', sep=" ", end="  ")
                                album_rating = album_track.userRating
                                # If the album track isn't rated, give it this track's rating
                                if album_rating is None:
                                    album_track.rate(comp_rating)
                                    album_track.reload()
                                elif album_rating != comp_rating:
                                    # If they aren't rated the same, apply the higher one
                                    if (comp_rating > album_rating):
                                        album_track.rate(comp_rating)
                                        album_track.reload()
                                    elif (album_rating > comp_rating):
                                        comp_track.rate(album_rating)  # We'll reload below
                                # Apply the "Dupe" mood
                                comp_track.addMood('Dupe')
                                comp_track.reload()
                                print('\033[1;31m' + "Marked" + '\033[0m')
