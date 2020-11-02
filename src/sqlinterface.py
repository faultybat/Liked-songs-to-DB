import sqlite3


def connect_to_database(dbname):
    try:
        db_conn = sqlite3.connect(dbname)
        return db_conn
    except:
        print("unable to connect to database")


def drop_music_table(db_name):
    db_conn = connect_to_database(db_name)
    cursor = db_conn.cursor()
    userInput = input("do you what to drop all tables (DEBUG) Y/N")
    if (userInput == "Y"):
        try:
            cursor.execute('''DROP TABLE artists''')
        except:
            print("artists dose not exist")
        try:
            cursor.execute('''DROP TABLE track''')
        except:
            print("track dose not exist")
        try:
            cursor.execute('''DROP TABLE albums''')
        except:
            print("albums dose not exist")

        try:
            cursor.execute('''DROP TABLE linker''')
        except:
            print("linker dose not exist")
    db_conn.commit()
    db_conn.close()


def create_tables(tablename):
    db_conn = connect_to_database(tablename)
    cursor = db_conn.cursor()
    #DEBUG TO DROP TABLE FOR SOME REASON
    #drop_music_table()
    # Creating track
    try:
        cursor.execute('''
                  CREATE TABLE track(track_id TEXT PRIMARY KEY,
                  track_name TEXT,track_length INTEGER , url TEXT,deleted INTEGER)
                  ''')
    except:
        print("track table probably alredy exists")

    # Creating artists

    try:
        cursor.execute('''
                  CREATE TABLE artists(artist_id TEXT PRIMARY KEY,
                  artist_name TEXT, url TEXT)
                  ''')
    except:
        print("artists table probably alredy exists")

    # Creating album

    try:
        cursor.execute('''
           CREATE TABLE albums(album_id TEXT PRIMARY KEY,
           album_name TEXT, url TEXT, release_data TEXT,
           album_image TEXT,image_witdth INTEGER, image_height INTEGER )
           ''')
    except:
        print("albums table probably alredy exists")

    # Creating linker
    try:
        cursor.execute('''
           CREATE TABLE linker(artist_ID TEXT NOT NULL,
           track_ID TEXT NOT NULL,
           album_ID TEXT NOT NULL,
           PRIMARY KEY (artist_ID,track_ID,album_ID),
           FOREIGN KEY (artist_ID) REFERENCES artists(artist_id),
           FOREIGN KEY (track_ID) REFERENCES track(track_id),
           FOREIGN KEY (album_ID) REFERENCES albums(album_id))
           ''')
    except:
        print("linker table probably alredy exists")
    db_conn.commit()
    db_conn.close()


def insert_track(entery,db_name):
    duration_ms = entery["track"]["duration_ms"]
    track_url = entery["track"]["external_urls"]["spotify"]
    track_name = entery["track"]["name"]
    track_id = entery["track"]["id"]
    deleted = 0

    db_conn = connect_to_database(db_name)
    cursor = db_conn.cursor()
    cursor.execute('''INSERT INTO track(
    track_id,
    track_name,
    track_length,
    url,
    deleted)
    VALUES(?,?,?,?,?)''', (track_id, track_name, duration_ms, track_url, deleted))
    db_conn.commit()
    #print(track_name)


def insert_artist(entery,db_name):
    artist_name_var = entery["track"]["artists"][0]["name"]
    artist_id = entery["track"]["artists"][0]["id"]
    artist_url = entery["track"]["artists"][0]["external_urls"]["spotify"]

    db_conn = connect_to_database(db_name)
    cursor = db_conn.cursor()

    try:
        cursor.execute('''INSERT INTO artists
           (artist_id,
           artist_name,
           url)
           VALUES(?,?,?)''', (artist_id, artist_name_var, artist_url))
        db_conn.commit()
    except:
        None
        #print("artist : " + artist_name_var + " alredy exists")


def insert_album(entery,db_name):
    album_name = entery["track"]["album"]["name"]
    album_id = entery["track"]["album"]["id"]
    album_url = entery["track"]["album"]["external_urls"]["spotify"]
    album_date = entery["track"]["album"]["release_date"]
    album_image_url = entery["track"]["album"]["images"][0]["url"]
    album_image_height = entery["track"]["album"]["images"][0]["height"]
    album_image_width = entery["track"]["album"]["images"][0]["width"]

    db_conn = connect_to_database(db_name)
    cursor = db_conn.cursor()

    try:
        cursor.execute('''INSERT INTO albums(
            album_id,
            album_name,
            url,
            release_data,
            album_image,
            image_witdth,
            image_height)
            VALUES(?,?,?,?,?,?,?)''', (
            album_id, album_name, album_url, album_date, album_image_url, album_image_height, album_image_width))
        db_conn.commit()
    except:
        None
        #print("album" + album_name + "alredy exists")


def insert_linker(entery,db_name):
    album_id = entery["track"]["album"]["id"]
    track_id = entery["track"]["id"]
    artist_id = entery["track"]["artists"][0]["id"]
    db_conn = connect_to_database(db_name)
    cursor = db_conn.cursor()

    cursor.execute('''INSERT INTO linker(
        artist_ID,
        track_ID,
        album_ID)
        VALUES(?,?,?)''', (artist_id, track_id, album_id))
    db_conn.commit()

def get_songid_to_comp(db1,db2):
    tblCmp = "SELECT * FROM track order by track_id"

    conn1 = sqlite3.connect(db1)
    conn2 = sqlite3.connect(db2)

    cursor1 = conn1.cursor()
    result1 = cursor1.execute(tblCmp)
    res1 = result1.fetchall()

    cursor2 = conn2.cursor()
    result2 = cursor2.execute(tblCmp)
    res2 = result2.fetchall()   
    return res1,res2 

def insert_songlist(songlist,db_name):
    for x in range(0, len(songlist)):
        #print(x)
        insert_track(songlist[x],db_name)
        insert_artist(songlist[x],db_name)
        insert_album(songlist[x],db_name)
        insert_linker(songlist[x],db_name)


def mark_deleted(deleted_song_id,db_name):
    db_conn = connect_to_database(db_name)
    cursor = db_conn.cursor()
    for x in range(0, len(deleted_song_id)):
        sql_update_query = """Update track set deleted = 1 where track_id = ?"""
        data = (deleted_song_id[x],)
        cursor.execute(sql_update_query, data)
        db_conn.commit()


#def check_change(songlist):



"""
def check_missing_song(songlist,db_name):
    db_conn = connect_to_database(db_name)
    cursor = db_conn.cursor()
    cursor.execute("SELECT track_id FROM track ORDER BY track_id ")
    rows = cursor.fetchall()
    song_id_list = []
    deleted_song_id = []
    for x in range(0, len(songlist)):
        song_id_list.append(songlist[x]["track"]["id"])
    song_id_list.sort()
    for x in range(0, len(songlist)):
        deleted = "true"
        for y in range(0, len(songlist)):
            if (song_id_list[y] == rows[x][0]):
                deleted = "false"
        if deleted == "true":
            print(rows[x][0] + " has been deleted")
            deleted_song_id.append(rows[x][0])
    db_conn.close()
    return deleted_song_id
"""