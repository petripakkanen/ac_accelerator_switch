# from mpd import MPDClient


class ACmpdPlayer:
    @staticmethod
    def checkClientState(cli):
        return cli.status()["state"]

    @staticmethod
    def nextSong(cli):
        cli.connect("localhost", 6600)
        if ACmpdPlayer.checkClientState(cli) == "play":
            print("Play next song.")
            cli.next()
        else:
            print("Player not playing")
        cli.disconnect()

    @staticmethod
    def play(cli):
        cli.connect("localhost", 6600)
        if ACmpdPlayer.checkClientState(cli) != "play":
            print("Start playing")
            cli.play()
            print(cli.status())
        else:
            print("Stop playing")
            cli.stop()
        cli.disconnect()
