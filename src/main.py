import sqlinterface
import getSpotifyData
import shutil
from pathlib import Path
import os


MAIN_DB_NAME = "liked_Songs.db"
TEMP_DB_NAME = "temp_new_songs.db"
OLD_DB_NAME = "old_liked_songs.db"


def check_if_ran():
    songlist = []
    songdatabase_file = Path(MAIN_DB_NAME)
    if (songdatabase_file.exists() == False):
        print("It looks to be the first time runing this program")
        userInput = input("Would you like to create a new database Y/N : ")
        if (userInput == "Y"):
            songlist = getSpotifyData.get_liked_songs()
            print("Creating tables this can take some time")
            sqlinterface.create_tables(MAIN_DB_NAME)
            print("Sorting and instering songlist into new db, this can take quite a bit of time")
            sqlinterface.insert_songlist(songlist,MAIN_DB_NAME)




def check_for_deleations():
##Checking if comparisons what to be ran
    userInput = input("do you what to check song diferances Y/N : ")
    if (userInput == "Y"):
        try : 
            os.remove(TEMP_DB_NAME)
        except :
            None
        #Coppying orignal db to new db for comparisions
        shutil.copy(MAIN_DB_NAME,OLD_DB_NAME)
        #Creating new temp from new data to perform comparision
        temp_songlist = getSpotifyData.get_liked_songs()
        print("Creating tables this can take some time")
        sqlinterface.create_tables(TEMP_DB_NAME)
        print("Sorting and instering songlist into new db, this can take quite a bit of time")
        sqlinterface.insert_songlist(temp_songlist,TEMP_DB_NAME)
        
        #Checking for deleations
        old_song_list,new_song_list = sqlinterface.get_songid_to_comp(MAIN_DB_NAME,TEMP_DB_NAME)
        old_song_list = set(old_song_list)
        new_song_list = set(new_song_list)
        result = old_song_list.symmetric_difference(new_song_list)
        for i in result :
            if i[0] in old_song_list :
                print("-------------------------------------------------")
                print(i[1] + " has been added to liked songs")
                print("It might be worth it to update the database")
                print("Once all deleated songs have been readded")
            if i[0] in new_song_list :
                print("-------------------------------------------------")
                print("Song : " + str(i[1]) + " is missing")
                print("The url to this song is : " + i[3])
        else:
            None

def debug():
    old_song_list,new_song_list = sqlinterface.get_songid_to_comp(MAIN_DB_NAME,TEMP_DB_NAME)
    old_song_list = set(old_song_list)
    new_song_list = set(new_song_list)
    result = old_song_list.symmetric_difference(new_song_list)
    old_song_list_ID = []
    new_song_list_ID = []
    for i in old_song_list:
        old_song_list_ID.append(i[0])
    for i in new_song_list:
        new_song_list_ID.append(i[0])
    for i in result :
        if i[0] in new_song_list_ID and (i[0] not in old_song_list_ID):
            None
            print("-------------------------------------------------")
            print(i[1] + " has been added to liked songs")
            print("It might be worth it to update the database")
            print("Once all deleated songs have been readded")
        if i[0] in old_song_list_ID and i[0] not in new_song_list_ID :
            print("-------------------------------------------------")
            print("Song : " + str(i[1]) + " is missing")
            print("The url to this song is : " + i[3])
    else:
        None


def main():
    #Checking if database has already been created
    #check_if_ran()
    #Checks for deleations in spotified liked playlist
    #check_for_deleations()
    debug()



main()
