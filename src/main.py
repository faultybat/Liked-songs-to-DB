import sqlinterface
import getSpotifyData

songlist = []
userInput = input("is this the first time runing  Y/N")
if (userInput == "Y"):
    songlist = getSpotifyData.get_liked_songs()
    sqlinterface.create_tables()
    sqlinterface.insert_songlist(songlist)

userInput = input("do you what to check song dif Y/N")
if (userInput == "Y"):
    if len(songlist) <= 0:
        songlist = getSpotifyData.get_liked_songs()
deleted_song_id = sqlinterface.check_missing_song(songlist)
sqlinterface.mark_deleted(deleted_song_id)
