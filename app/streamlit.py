import streamlit as st
import pandas as pd
import tweepy
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import ccxt
import altair as alt

load_dotenv()

st.sidebar.title("Navigator")
option = st.sidebar.selectbox("Dashboard Selector", ('Twitter', 'Bitcoin'))
st.title(option)

if option == 'Twitter' : 
    
    # We can define columns for the webpage and asign charts/texts/... to each column.
    # These columns are going to be in parallel to each other 
    # col1, col2 = st.columns(2)
    

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

if option == 'Bitcoin' : 
    exchange = ccxt.kraken()

    # markets = exchange.load_markets()
    # for market in markets:
    #     print(market)

    # Get historical prices for Bitcoin
    ohlcv_btc = exchange.fetch_ohlcv('BTC/USD', '1d')
    ohlcv_eth = exchange.fetch_ohlcv('ETH/USD', '1d')


    # Print the historical prices
    btc = pd.DataFrame(ohlcv_btc)
    btc["Date"] = pd.to_datetime(btc[0], unit='ms')
    # btc = btc.set_index('Date')
    btc = btc.drop([0,5],axis=1)

    eth = pd.DataFrame(ohlcv_eth)
    eth["Date"] = pd.to_datetime(eth[0], unit='ms')
    # btc = btc.set_index('Date')
    eth = eth.drop([0,5],axis=1)

    # Renaming columns
    btc = btc.rename(columns={1: "Open", 2: "High", 3: "Low", 4: "Close"})
    eth = eth.rename(columns={1: "Open", 2: "High", 3: "Low", 4: "Close"})

    btc['coin'] = 'btc'
    btc = btc[['Date', 'coin', 'Open', 'High', 'Low', 'Close']]

    eth['coin'] = 'eth'
    eth = eth[['Date', 'coin', 'Open', 'High', 'Low', 'Close']]

    #join
    # joined = pd.concat([btc,eth], axis=1)
    # joined = joined.drop('Date_eth', axis=1)
    # joined = joined.rename(columns={'Date_btc': 'Date'})

    # Union
    unioned = pd.concat([btc, eth])

    # Altair Charts
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Date'], empty='none')

    line = alt.Chart(unioned).mark_line(interpolate='basis').encode(
        x='Date',
        y='Close',
        color='coin:N'
    )

    selectors = alt.Chart(unioned).mark_point().encode(
        x='Date',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'Close', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(unioned).mark_rule(color='gray').encode(
        x='Date',
    ).transform_filter(
        nearest
    )

    chart = alt.layer(
        line, selectors, points, text, rules
    ).properties(
        width=600, height=300
    )

    chart