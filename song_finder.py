import pandas as pd 
import numpy as np 
import webbrowser
pd.options.mode.chained_assignment = None

df = pd.read_pickle('./data/music.pkl')


def find_song(df,song = False,artist = False):
    if song == False and artist == False:
        return 'no song or artist inserted'
    df1 = df.loc[df['track_name'] == song]
    if len(df1) == 1:
        return df1
    
    if artist != False:
        if any(df1['artist_name'] == artist) == True:
            df1 = df1.loc[df1['artist_name'] == artist]
        else:
            return 'artist not found'
        
        if(len(df1) <= 1):
            return df1
        else:
            df1['popularity'] = pd.to_numeric(df1['popularity'])
            return df1.loc[df1['popularity'].idxmax()]           #return most popular of the songs
        
    
    else:
        df1['popularity'] = pd.to_numeric(df1['popularity'])
        return df1.loc[df1['popularity'].idxmax()]           #return most popular of the songs



def access(df):
		if(type(df['track_id'])) == str:
				open_spotify = 'https://open.spotify.com/embed/track/' + df['track_id']
		else:
				open_spotify ='https://open.spotify.com/embed/track/'  + str(df['track_id'].iloc[0])
		
		webbrowser.open(open_spotify)

