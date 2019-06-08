import pandas as pd 
import webbrowser
class Song:

    def __init__(self,track_name: str = None,artist_name: str = None,track_id: str = None,genre: str = None,popularity: float = None,valence: float = None,danceability: float = None,energy: float = None,loudness: float = None):
        self.genre = genre
        self.artist_name = artist_name
        self.track_id = track_id
        self.track_name = track_name
        self.popularity = popularity
        self.valence = valence
        self.danceability = danceability 
        self.energy = energy
        self.loudness = loudness
        


    def play(self):
        _play = 'https://open.spotify.com/embed/track/' + self.track_id
        webbrowser.open(_play)
            
    def play_genre(self,df):
        genre_df = df.loc[df['genre'] == self.genre]
        genre_df = genre_df.sort_values('popularity',ascending = False)
        genre_df = genre_df[:100].sample()
        track    = Song(track_id = str(genre_df['track_id'].iloc[0]))
        return genre_df
        validation(df,)
        #track.play()

    def play_sad(self,df):
        df = df.sort_values('valence')
        bad_mood = df.loc[df['valence'] != '0.0']
        bad_mood = bad_mood[:400]
        bad_mood = bad_mood.sort_values('popularity',ascending = False)
        track    = bad_mood[:200].sample()
        print(track)
        track    = Song(track_id = track['track_id'].iloc[0])
        track.play()

    def play_happy(self,df):
        df = df.sort_values('valence',ascending = False)
        df = df[:400]
        df = df.sort_values('popularity',ascending = False)
        track  = df[:200].sample()
        print(track)
        track  = Song(track_id = track['track_id'].iloc[0])
        track.play()




def get_nouns(dic):
    words = []
    for entity in dic['entities']:
        if entity['type'] == 'NN':
            words.append(entity['text'])
    return words



def g_label(dic,genres):
    words = get_nouns(dic)
    for word in words:
        if word in genres:
            return Song(genre = word)





def validation(df,classifier):
    play_tags = ['ok']
    retry_tags = ['no']
    play_t = ['ok']
    retry = ['no']
    print('what do you think about ',df['track_name'].iloc[0])
    print('\n')
    user_input = input()
    user_input = user_input.split(' ') 
    for word in user_input:
        print(word)
        if word in play_tags:
             user_song.track_id = df['track_id'].iloc[0]
             user_song.play()
        elif word in retry_tags:
             retry_song = user_song.play_genre()
             



              
        