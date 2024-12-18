import requests 
import pandas as pd
from Transform import df_clean
import Api_calls
import config
from Transform import df_clean


def get_azure_sentiment(text: str) -> dict:
    header = { 'X-API-KEY': config.APIKEY }
    data = { "text" : text }
    url = "https://cent.ischool-iot.net/api/azure/sentiment"
    response = requests.post(url, headers=header, data=data)
    response.raise_for_status()
    return response.json() 

#----------------------------------------------

CACHE_SIMS_FILE = "df_best.csv"


Sims4_df = df_clean

# getting the sentiments based on each comment 
sentiments = []
for index, row in Sims4_df.iterrows():
    sentiment = get_azure_sentiment(row['selftext'])
    sentiment_item = sentiment['results']['documents'][0]
    sentiment_item['title'] = row['title']
    sentiment_item['selftext'] = row['selftext']
    sentiment_item['upvote_ratio'] = row['upvote_ratio']
    sentiment_item['ups'] = row['ups']
    sentiments.append(sentiment_item)

    sentiment_df = pd.json_normalize(sentiments, record_path="sentences", meta=['title', 'selftext', 'upvote_ratio', 'ups'])

    # rename text column to sentence_text and sentence_sentiment
    sentiment_df.rename(columns={'selftext': 'sentence_text'}, inplace=True)
    sentiment_df.rename(columns={'sentiment': 'sentence_sentiment'}, inplace=True)

    # filter output: selftext, sentence_text, sentence_sentiment
    filter_sentiment_df = sentiment_df[['title', 'sentence_text', 'sentence_sentiment', 'confidenceScores.positive', 'confidenceScores.neutral', 'confidenceScores.negative', 'upvote_ratio', 'ups']]

    # filter so the selftext rows with the best confidence score based on each title is kept and the rest are dropped
    filter_sentiment_df['max_confidence_score'] = filter_sentiment_df[['confidenceScores.positive', 'confidenceScores.neutral', 'confidenceScores.negative']].max(axis=1)
    
    # Sort the DataFrame by title and max_confidence_score in descending order
    df_sorted = filter_sentiment_df.sort_values(by=['title', 'max_confidence_score'], ascending=[True, False])
    
    # Drop duplicates to keep only the row with the highest confidence score for each title
    df_best = df_sorted.drop_duplicates(subset=['title'], keep='first')
    


    # save to cache, return dataframe
    df_best.to_csv(CACHE_SIMS_FILE, index=False, header=True)



import streamlit as st 
#st.dataframe(df_best)
# st.write(df_best)
