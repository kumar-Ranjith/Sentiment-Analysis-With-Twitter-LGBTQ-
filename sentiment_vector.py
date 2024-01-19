import pandas as pd
import nltk
import ssl
import re
import random
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from sklearn.linear_model import LogisticRegression


# use this code to import the twitter training data
'''
import ssl
import nltk
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

#nltk.download('twitter_samples')
#nltk.download('stopwords')

'''

from nltk.corpus import twitter_samples
from nltk.corpus import stopwords

# variables for our model
alphaNum = r'[a-zA-Z0-9]+'
tokenizer = RegexpTokenizer(alphaNum)
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
pos_tweets = twitter_samples.strings('positive_tweets.json')
neg_tweets = twitter_samples.strings('negative_tweets.json')
text = twitter_samples.strings('tweets.20150430-223406.json')
stop_words = set(stopwords.words('english'))
vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')
tweets = pd.read_csv("sampled_tweets.csv", lineterminator='\n')
tweets.dropna(inplace = True)


# removes @signs, hashtags, and links from tweets
def removeNoise(text):
    text = re.sub(r'#', '', str(text)) #removes tags
    text = re.sub(r'@[A-Za-z0-9]+', "", str(text)) #removes mentions
    text = re.sub(r'https?:\/\/t.co\/[A-Za-z0-9]+', '', str(text)) #removes links
    return text

# tokenizes tweets
def tokenize_tweets(tweets):
    tokenized_tweets = [tokenizer.tokenize(removeNoise(tweet)) for tweet in tweets]
    return tokenized_tweets

# stems tweets
def stem_tweets(tweets):
    return [[stemmer.stem(token) for token in tweet] for tweet in tweets]

#lemmatizes tweets
def lemmatize_tweet(tweet):
    str = ""
    for token in tweet:
        str += lemmatizer.lemmatize(token)
    return str

# removes stopwords (unused)
def remove_Stopwords(tweets):
    return [[token for token in tweet if token.lower() not in stop_words] for tweet in tweets]


#create a training dataset and shuffle
positive_dataset = [[lemmatize_tweet(removeNoise(tweet)), "Positive"] for tweet in pos_tweets]
negative_dataset = [[lemmatize_tweet(removeNoise(tweet)), "Negative"] for tweet in neg_tweets]
dataset = positive_dataset + negative_dataset
random.shuffle(dataset)

# use our functions to score tweets.
tweets["clean_text"] = tweets["text"].apply(removeNoise).apply(lemmatize_tweet)


#split into test and training
train_data = dataset[:7000]
test_data = dataset[7000:]


train_db = pd.DataFrame(train_data, columns = ["text", "sentiment"])
test_db = pd.DataFrame(test_data, columns = ["text", "sentiment"])

#vectorize our datasets
train_matrix = vectorizer.fit_transform(train_db['text'])
test_matrix = vectorizer.transform(test_db['text'])
test_matrix_tweets = vectorizer.transform(tweets['clean_text'].values.astype('U'))

# create our model
lr_model = LogisticRegression()
X_train = train_matrix
X_test = test_matrix
X_test_tweets = test_matrix_tweets
Y_train = train_db['sentiment']
Y_test = test_db['sentiment']

lr_model.fit(X_train,Y_train)
Y_pred = lr_model.predict(X_test)
Y_pred_tweets = lr_model.predict(X_test_tweets)

# add sentiment to table
tweets["sentiment"] = Y_pred_tweets
tweets.drop('clean_text', axis=1, inplace=True)

#write it to file
tweets.to_csv("scored_tweets_vectorization.csv", lineterminator='\n')

#print accuracy score for training dataset
print(accuracy_score(Y_pred, Y_test))










#tokens = tokenizer.tokenize()

#stemmed_tokens = [stemmer.stem(token) for token in tokens]



