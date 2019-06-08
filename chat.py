import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import pandas as pd
from flair.models import TextClassifier
from flair.data import Sentence
from music import *
import sys
from flair.models import SequenceTagger
import webbrowser

play_tags = ['ok']
retry_tags = ['no']
part_of_speech = 'pos'
#model loadings
tagger = SequenceTagger.load('pos')
mood = TextClassifier.load('en-sentiment')
classifier = TextClassifier.load_from_file(sys.argv[1])

def runApplication():
	text = get_generic_input()
	runClassifier(text)

def runClassifier(text):
	print('Running classifier for "', text, '"')
	sentence = generic_input_classifier(text)
	if is_genre(sentence):
		print('Is genre.')
		genre = get_genre(sentence)
	elif is_mood(sentence):
		print('Is mood.')
		mood_history.append(get_mood(sentence))
		print(mood_history)
	runSuggestionLoop()

def runSuggestionLoop():
	print('Running suggestion loop.')
	suggestion = get_suggestion()
	reply = get_suggestion_reply(suggestion)
	if reply == 'play':
		print('Playing.')
		play(suggestion)
	elif reply == 'retry':
		print('Retrying.')
		runSuggestionLoop()
	else:
		print('Running classifier again.')
		runClassifier(reply)

def get_generic_input():
	print('How are you feeling today? Or which genre would you like to listen to?\n')
	generic_input = input()
	return generic_input

def generic_input_classifier(text):
	sentence = Sentence(text)
	classifier.predict(sentence)
	tagger.predict(sentence)	
	return sentence

def is_genre(sentence):
	return ((sentence.get_label_names()[0]) == 'g')

def is_mood(sentence):
	return ((sentence.get_label_names()[0]) == 'm')

def get_genre(sentence):
	dic = sentence.to_dict(part_of_speech)
	song_g = g_label(dic,genres)
	#dar um jeioto de retornar o genre
	return 'rock'		

def get_mood(sentence):
	mood.predict(sentence)
	return sentence
	#return ("NEGATIVE", 1)

def get_suggestion():
	suggestion = df
	if current_genre != False:
		suggestion = df.loc[df['genre'] == current_genre]
	if len(mood_history) >= 1:
		last_mood = mood_history[-1]
		print('last_mood: ', last_mood)
		negative = (last_mood.get_label_names()[0] == 'NEGATIVE')
		suggestion = suggestion.sort_values('valence',ascending = negative)
			
	suggestion = suggestion[:400]
	suggestion = suggestion.sort_values('popularity',ascending = False)
	return suggestion[:200].sample() 

def get_suggestion_reply(suggestion):
	print('what do you think about ', get_track_name(suggestion))
	print('\n')
	reply = input()
	for word in reply.split(' '):
		if word in play_tags:
			return 'play'
		elif word in retry_tags:
			return 'retry'
	return reply

def get_track_name(suggestion):
	return suggestion['track_name'].iloc[0]

def play(suggestion):
	track_id = suggestion['track_id'].iloc[0]
	_play = 'https://open.spotify.com/embed/track/' + track_id
	webbrowser.open(_play)
	print('What next?')
	text = input()
	runClassifier(text)






df = pd.read_pickle('./data/music.pkl')
df = df.loc[df['valence'] != '0.0']

genres = set(df['genre'])

mood_history = []
current_genre = False

#aqui começa tudo
runApplication()




