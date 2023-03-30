import re
from nltk.corpus import stopwords
from textblob import TextBlob

stop_words = stopwords.words('english')

def clean_tweet(tweet):
    """Clean a singular tweet"""
    clean_tweet = re.sub(r"@[a-zA-z0-9_]+", "", tweet)
    clean_tweet = re.sub(r"#[a-zA-z0-9_]+", "", clean_tweet)
    clean_tweet = ' '.join(word for word in clean_tweet.split() if word not in stop_words)
    return clean_tweet


def get_polarity(tweet):
    """Fetches polarity of a tweet / text"""
    return TextBlob(tweet).sentiment.polarity


def get_subjectivity(tweet):
    """Fetches subjectivity of a tweet / text"""
    return TextBlob(tweet).sentiment.subjectivity


def analyze_text(polarity):
    """Returns positive, neutral or negative of cleaned text"""
    if polarity > 0:
        return 'positive'
    elif polarity == 0:
        return 'neutral'
    else:
        return 'negative'
