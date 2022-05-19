# PlexScripts
Various simple (typically single-task) scripts for managing media on a Plex server.

## **Let me say up front . . .**
. . . that I'm relatively new and largely self-taught when it comes to both Git and Python. So I probably do things in not-the-most-efficient ways pretty regularly. If you have any advice for better methods to accomplish anything here, by all means please let me know.

## **Requirements**
Obviously, you need to have a running Plex server.

You'll also need Python, on the computer where you're running these (not necessarily on the server itself). To make these scripts useful for you, it will probably help to have at least a passing comfort level with tweaking a Python script. I'll make it pretty obvious where & how to change things, where I can.

### **Dependencies**
You'll need to install the [PlexAPI](https://python-plexapi.readthedocs.io/en/latest/introduction.html) package.

Some of the scripts may make use of other packages, but usually nothing too exotic—`collections`, `glob`, `os`, `re`, etc. For now, I'm going to leave you to figure these out from the `import` lines in the scripts themselves. But if there's anything too unusual or if something seems to keep popping up in numerous scripts, I'll make a note of it here.

## **Authentication**
Authentication is accomplished by means of a [PlexAPI config file](https://python-plexapi.readthedocs.io/en/latest/configuration.html). It's really easy to set up, and keeps that information securely out of potentially public folders like this git repository.
