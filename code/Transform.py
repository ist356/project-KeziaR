import pandas as pd
import streamlit as st
from Api_calls import df
import re

# Finally I want to save the data to a csv file
# but first I need to remove the emojis

def clean_data(df):

    # Many text have emojis, so they will be removed
    df['title'] = df['title'].str.encode('ascii', 'ignore').str.decode('ascii')

    # Remove duplicated titles
    df.drop_duplicates(subset=['title'], keep='first', inplace=True)

#----------------------------------------------
    # Many text have emojis, so they will be removed
    df['selftext'] = df['selftext'].str.encode('ascii', 'ignore').str.decode('ascii')

    # Remove rows where 'selftext' is blank
    df = df[df['selftext'].notna()]


    # Remove rows where 'selftext' contains a URL
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    df = df[~df['selftext'].str.contains(url_pattern, na=False)]
 

    # Remove rows where 'selftext' has less than 2 words
    df = df[df['selftext'].str.split().str.len() >= 2]

    

    return df



#----------------------------------------------
# combine both dataframes into one
df = pd.read_csv("Sims4_data.csv")

df_clean = clean_data(df)

df_clean.to_csv("Sims4_new.csv", index=False)

#st.dataframe(df_clean)



# @st.cache_data
# def convert_df(df):
#     return df.to_csv().encode('utf-8')

# csv = convert_df(df)
# st.download_button(
#     "Download CSV",
#     csv,
#     "sims4_subreddit_data.csv",
#     "text/csv",
#     key='download-csv'
# )






#----------------------------------------------
# Importing into a streamlit so I
# can view the data better