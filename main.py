import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utilities import clean_tweet
from utilities import get_polarity
from utilities import get_subjectivity
from utilities import analyze_text
from wordcloud import WordCloud
from time import sleep
import getpass

# Show entire df content
# pd.set_option('display.max_colwidth', 250)
search_item = "Elon Musk"
window_scroll = 'window.scrollTo(0, document.body.scrollHeight);'


def main():
    try:
        my_user = "dan_writescode"
        my_pass = getpass.getpass(prompt='Please enter your twitter pass: ')
        driver = webdriver.Chrome()
        driver.get("https:/twitter.com/i/flow/login")
        sleep(3)

        # find login element by XPATH and send username
        user_id = driver.find_element(By.XPATH, '//input[@autocomplete="username"]')
        user_id.send_keys(my_user)

        next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
        next_button.click()

        sleep(3)
        password = driver.find_element(By.XPATH, "//input[@name='password']")
        password.send_keys(my_pass)

        login_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Log in')]")
        login_button.click()

        sleep(3)
        # Search for the search item defined in global scope
        search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
        search_box.send_keys(search_item)
        search_box.send_keys(Keys.ENTER)

        tweets_collection = set()
        tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")

        # Scrape tweet text
        while len(tweets_collection) <= 50:
            for tweet in tweets:
                tweets_collection.add(tweet.text)
            driver.execute_script(script=window_scroll)
            sleep(3)
            tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")

        tweets_collection = list(tweets_collection)
        df = pd.DataFrame(tweets_collection, columns=['tweets'])

        # Create new column containing cleaned tweets
        df['cleaned_tweets'] = df['tweets'].apply(clean_tweet)
        df['tweet_polarity'] = df['cleaned_tweets'].apply(get_polarity)
        df['tweet_sub'] = df['cleaned_tweets'].apply(get_subjectivity)
        df['segmentation'] = df['tweet_polarity'].apply(analyze_text)

        print(df.pivot_table(index=['segmentation'], aggfunc={'segmentation': 'count'}))
        print(df.sort_values(by=['tweet_polarity'], ascending=False).head(3))
        print(df.sort_values(by=['tweet_polarity'], ascending=True).head(3))
        print(df[df['tweet_polarity'] == 0].head(3))

        consolidated_words = ' '.join(word for word in df['cleaned_tweets'])

        # Generate word cloud based off consolidated word string
        cloud = WordCloud(width=500, height=300, max_font_size=120).generate(consolidated_words)

        plt.imshow(cloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

        plt.figure(figsize=(10,8))
        sns.set_style("darkgrid")
        sns.scatterplot(data=df, x='tweet_polarity', y='tweet_sub', s=100, hue="segmentation")
        plt.title('Tweet Polarity vs Subjectivity')
        plt.show()

        sns.countplot(data=df, x='segmentation')
        plt.title(f'Tweet polarity counts for search term {search_item}')
        plt.show()

    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    main()
