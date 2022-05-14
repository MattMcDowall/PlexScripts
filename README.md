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

## **A note on authentication**
PlexAPI allows a [couple of different methods](https://python-plexapi.readthedocs.io/en/latest/introduction.html#getting-a-plexserver-instance) to get a server instance to work with. I'm trying to keep these scripts agnostic on that decision, and also to keep the credentials private. My approach is to tackle the authentication and get a server instance from an external file, and then call that file from these scripts.

What I've done is to create a script called `Credentials.py` which resides in this folder on my computer. To keep it private, I've added a line in the `.gitignore` file which filters it out of any pushes to the public repository. So you'll need to create your own Credentials.py file, in this same directory.

Depending on which method of authentication you prefer, the contents of Credentials.py look either like this:

    def plex_connect():
        from plexapi.myplex import MyPlexAccount
        account = MyPlexAccount('<USERNAME>', '<PASSWORD>')
        return(account.resource('<SERVERNAME>').connect())

or like this:

    def plex_connect():
        from plexapi.server import PlexServer
        baseurl = 'http://plexserver:32400'
        token = '2ffLuB84dqLswk9skLos'
        return(PlexServer(baseurl, token))

Then, as you can see in the scripts themselves, we get the server instance with these two lines:

    import Credentials # <=== This is calling your external script
    plex = Credentials.plex_connect() # <=== You can now reference the
                                      #      server instance as *plex*

I hope that makes sense.

All of these scripts will rely on you having this setup, or knowing how to tweak things to adjust for your different setup.
