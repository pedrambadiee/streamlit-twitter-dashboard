import streamlit as st
import pandas as pd
import tweepy
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

load_dotenv()

st.sidebar.title("Navigator")
option = st.sidebar.selectbox("Dashboard Selector", ('Twitter', 'Bitcoin'))
st.title(option)

if option == 'Twitter' : 
    """
    We can define columns for the webpage and asign charts/texts/... to each column.
    These columns are going to be in parallel to each other 
    col1, col2 = st.columns(2)
    """

# Get your twitter credentials:
    api_key = os.getenv('api_key')
    api_key_secret = os.getenv('api_key_secret')
    access_token = os.getenv('access_token')
    access_token_secret = os.getenv('access_token_secret')
    bearer_token = os.getenv('bearer_token')

    Client = tweepy.Client(bearer_token=bearer_token)

    keyword = st.sidebar.text_input("Keyword")
    granularity = st.sidebar.selectbox("TimeFrame", ('day', 'hour', 'minute'))
    if keyword != "" :
        recent_tweets = Client.get_recent_tweets_count(query={keyword}, granularity={granularity})
        df = pd.DataFrame(recent_tweets.data)
        df = df[['end', 'tweet_count']]
        fig, ax = plt.subplots()
        ax.plot('end', 'tweet_count', data=df[1:-1])
        """
        If you want to asign the chart below to a column you can:
        with col1 :
        """
        st.pyplot(fig)

        st.dataframe(df,700,250)