import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

"""

This function processes the song file so that we can insert the data into the songs and artists tables. We first read the song files, 
then we insert the data into the songs table and finally we insert the data into the artists tables.

INPUTS:
* cur - cursor variable
* filepath - path for the song file we are reading and pulling in

"""

def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = song_data.values[0]
    song_data.tolist()
    cur.execute(song_table_insert, song_data)


    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = artist_data.rename({'artist_name': 'name', 'artist_location': 'location', 'artist_latitude': 'latitude', 'artist_longitude': 'longitude'})
    artist_data = artist_data.values[0]
    artist_data.tolist()
    cur.execute(artist_table_insert, artist_data)

"""

This function processes the log file so that we can insert the data into the time, users and songplays tables. We first read the log files, 
then we insert the data into the times table, next the users table and finally we insert the data into the songplays tables.

INPUTS:
* cur - cursor variable
* filepath - path for the log file we are reading and pulling in

"""

def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] =='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day,t.dt.isocalendar().week, t.dt.month, t.dt.year,t.dt.weekday)
    column_labels = ('start_time','hour','day','week','month','year','weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))


    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df = user_df.rename({'userId': 'user_id', 'firstName': 'first_name', 'lastName': 'last_name'})

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit = 'ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)

"""

Here we execute the functions we established above to connect to the database, process the song and log file 
and inset the data into our tables before disconnection from the database.

INPUTS:
* cur - cursor variable
* conn - connects to the database
* filepath - path for the song file we are reading and pulling in
* func - establishes either the process song file function or the process log file function we created earlier

"""

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()