# For details on this script, see the README.md file in this repo

from plexapi.myplex import MyPlexAccount

print('Connecting to server . . .')
account = MyPlexAccount()   # Credentials retrieved from PlexAPI config.ini file
print('    . . . connection established.')
plex = account.resource('MEDIA').connect()

for collxnTitle in ["Compilations", "Anthologies"]:
    for collxn in plex.library.section('Music').search(filters={"title==": collxnTitle}, libtype="collection"):
        for album in collxn.items():
            print(album.parentTitle, '|', album.title, sep=' ')
            for compTrack in album.tracks():
                # - To speed things up, also limit to *rated* tracks
                # - Seems to crash if the track title begins with an apostrophe, so skip those
                # - Skip any that are already marked as dupes
                if ((compTrack.userRating is not None) & (not compTrack.title.startswith("'")) & (all(m.tag != "Dupe" for m in compTrack.moods))):
                    # Search for:
                    #   *exact* title match AND
                    #   *non-matching* id (ratingKey) AND
                    #   matching track isn't marked as a Dupe
                    for albumTrack in plex.library.section('Music').search(filters={"title==": compTrack.title, "track.id!=": compTrack.ratingKey, "track.mood!=": "Dupe"}, libtype='track'):
                        # Check the difference in lengths
                        # Looking for an arbitrary threshold of <8 seconds difference
                        if(abs(albumTrack.duration - compTrack.duration) < 8000):
                            # Can't filter for artist name, so double-check it
                            #   "originalTitle" is the track artist
                            #   "grandparentTitle" is the album artist, which we check on
                            #       the album track in case the originalTitle isn't set (it
                            #       often isn't, if it's the same as the album artist for
                            #       all tracks).
                            if (albumTrack.originalTitle == compTrack.originalTitle) or (albumTrack.grandparentTitle == compTrack.originalTitle):
                                print('  ', compTrack.ratingKey, compTrack.originalTitle, compTrack.title, sep="\t")
                                print("\t\tDupe of:", albumTrack.ratingKey, albumTrack.title, '[' + albumTrack.parentTitle + ']', sep=" ", end="  ")
                                compRating = compTrack.userRating
                                albumRating = albumTrack.userRating
                                # If they aren't rated the same, apply the higher of the two
                                if ((albumRating is not None) and (compRating is not None) and (albumRating != compRating)):
                                    if (compRating > albumRating):
                                        albumTrack.rate(compRating)
                                        albumTrack.reload()
                                    elif (albumRating > compRating):
                                        compTrack.rate(albumRating)  # We'll reload below
                                # Apply the "Dupe" mood
                                compTrack.addMood('Dupe')
                                compTrack.reload()
                                print('\033[1;31m' + "Marked" + '\033[0m')
