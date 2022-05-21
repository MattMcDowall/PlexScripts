# MarkDupes

## Purpose
Checks songs on Compilation & Anthology albums, to see if you have the same song on a regular album. If so, marks the comp/anth version as “Dupe” (as a Mood) so it can be automatically excluded from Smart Playlists.

## A note on terms
I’m using `compilation` to refer to an album that has tracks from different artists—a soundtrack, for instance, or a record-company retrospective box set.

An `anthology` is an album consisting mostly of previously released material, but all from the same artist. The typical example would be a *Greatest Hits* album.

## Requirements
This script requires you to have two collections in Plex—**Compilations,** and **Anthologies.** You’ll have to manually add these (note that they are *album* collections, not tracks), and you’ll need to add the appropriate albums into them.

> You could potentially tweak it to get the *compilations* on the fly, by looking for any track with “Various Artists” as the `grandparentTitle` (album artist). There’s no effective way to do that for anthologies, though.
