import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import pandas as pd
from flair.models import TextClassifier
from flair.data import Sentence
import sys
from flair.models import SequenceTagger
import webbrowser
import re
import os

debug = False
play_tags = ['ok','play','yes','sure','like','love','awesome','nice','yep','yeah','good']
retry_tags = ['no','next','shuffle','hate','dislike','another','nope','nay','jeez','nah','ugh','not']
#model loadings

tagger = SequenceTagger.load('pos')
mood = TextClassifier.load('en-sentiment')
classifier = TextClassifier.load(sys.argv[1])
df = pd.read_pickle('./data/music.pkl')
df = df.loc[df['valence'] != '0.0']

genres = set(df['genre'])

mood_history = []
current_genre = False

def debug_print(*objects):
	global debug
	if(debug):
		print(objects)


def runApplication():
	text = get_generic_input()
	runClassifier(text)


def runClassifier(text):
	global current_genre, mood_history
	if len(text) == 0:
		runApplication()
		return
	debug_print('Running classifier for "', text, '"')
	sentence = generic_input_classifier(text)
	debug_print("sentence: ", sentence)
	if is_genre(sentence):
		debug_print('Is genre.')
		current_genre = get_genre(sentence)
		debug_print('Current genre: ', current_genre)
	elif is_mood(sentence):
		debug_print('Is mood.')
		mood_history.append(get_mood(sentence))
		debug_print(mood_history)
	elif is_specific(sentence):
		debug_print('Is specific.')
		text = text.split()
		if text[0].lower() == 'play':
			text = text[1:]
		text = re.sub('\s','%20',' '.join(text))
		text2url = 'https://open.spotify.com/search/results/' + text
		webbrowser.open(text2url)
		runApplication()


	runSuggestionLoop()

def runSuggestionLoop():
	debug_print('Running suggestion loop.')
	suggestion = get_suggestion()
	reply = get_suggestion_reply(suggestion)
	if reply == 'play':
		debug_print('Playing.')
		play(suggestion)
	elif reply == 'retry':
		debug_print('Retrying.')
		runSuggestionLoop()
	else:
		debug_print('Running classifier again.')
		runClassifier(reply)

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
            return word

def get_generic_input():
	print('How are you feeling today? Or what would you like to hear?\n')
	generic_input = input()
	return generic_input

def generic_input_classifier(text):
	global classifier, tagger
	sentence = Sentence(text)
	classifier.predict(sentence)
	tagger.predict(sentence)	
	return sentence

def is_genre(sentence):
	return ((sentence.get_label_names()[0]) == 'g')

def is_mood(sentence):
	return ((sentence.get_label_names()[0]) == 'm')	

def is_specific(sentence):
	return ((sentence.get_label_names()[0]) == 's')	

def get_genre(sentence):
	global genres
	dic = sentence.to_dict('pos')
	return g_label(dic, genres)

def get_mood(sentence):
	global mood
	mood.predict(sentence)
	return sentence
	#return ("NEGATIVE", 1)

def get_suggestion():
	global df
	debug_print("Generating suggestion")
	suggestion = df
	debug_print('get_suggestion() current_genre: ', current_genre)
	if current_genre != False:
		debug_print("Has genre: ", current_genre)
		suggestion = suggestion.loc[df['genre'] == current_genre]
	if len(mood_history) >= 1:
		last_mood = mood_history[-1]
		debug_print('last_mood: ', last_mood)
		negative = (last_mood.get_label_names()[0] == 'NEGATIVE')
		suggestion = suggestion.sort_values('valence',ascending = negative)
			
	suggestion = suggestion[:400]
	suggestion = suggestion.sort_values('popularity',ascending = False)
	return suggestion[:200].sample() 

def get_suggestion_reply(suggestion):
	global play_tags, retry_tags
	print('\nWhat do you think about \nArtist: ', get_artist(suggestion), '\nTrack: ', get_track_name(suggestion), '\nGenre: ', get_track_genre(suggestion), '\n')
	reply = input()
	for word in reply.split(' '):
		if word in play_tags:
			return 'play'
		elif word in retry_tags:
			print('\nhmmm... ok\n')
			return 'retry'
	return reply

def get_track_name(suggestion):
	return suggestion['track_name'].iloc[0]

def get_artist(suggestion):
	return suggestion['artist_name'].iloc[0]

def get_track_genre(suggestion):
	return suggestion['genre'].iloc[0]

def play(suggestion):
	track_id = suggestion['track_id'].iloc[0]
	_play = 'https://open.spotify.com/embed/track/' + track_id
	webbrowser.open(_play)
	print('What next?')
	text = input()
	runClassifier(text)

#start
if __name__ == '__main__':
    os.system('clear')
    runApplication()


