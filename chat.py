import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import pandas as pd
from flair.models import TextClassifier
from flair.data import Sentence
from music import *
import sys
from flair.models import SequenceTagger

#model loadings
tagger = SequenceTagger.load('pos')
mood = TextClassifier.load('en-sentiment')
classifier = TextClassifier.load_from_file(sys.argv[1])

df = pd.read_pickle('./data/music.pkl')
genres = set(df['genre'])
user = 'I am really sad'     #for testing only

sentence = Sentence(user)
classifier.predict(sentence)
tagger.predict(sentence)	

if (sentence.get_label_names()[0]) == 'g':
	dic = sentence.to_dict('pos')
	aux = g_label(dic,genres)
	aux.play_genre(df)

if (sentence.get_label_names()[0]) == 'm':
	user_mood = user                     		#sentiment analysis
	user_mood = Sentence(user_mood)
	mood.predict(user_mood)
	if user_mood.get_label_names()[0] == 'NEGATIVE':
		play_sad(df)
	else:
		pass



