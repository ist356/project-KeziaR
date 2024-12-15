import pandas as pd
import streamlit as st
import requests
import config

# starting off by gaining access to the reddit API


auth = requests.auth.HTTPBasicAuth(config.Client_ID, config.Secret_Key)



data = {
    'grant_type': 'password',
    'username': config.auth1,
    'password': config.auth2
}

headers = {
    'User-Agent': 'MyAPI/0.0.1'
    }

#----------------------------------------------

# Now I am getting token access to the API


TOKEN_ACCESS = 'https://www.reddit.com/api/v1/access_token'
res = requests.post(TOKEN_ACCESS, 
                   auth=auth, data=data, headers=headers)


if res.status_code == 200:
    TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'

#----------------------------------------------

# In the function I want to 
# make getting posts easier
# by not hardcoding the parameters
# and by combining the dataframes into one

def get_posts(endpoint, query, sort, limit=100):

    params = {
            'q': query,
            'restrict_sr': 'on',
            'sort': sort,
            't': 'all',
            'limit': limit
        }

    all_posts = []  

#----------------------------------------------
    # part about pagination that I will use to get more posts

    while True:
        response = requests.get(endpoint, headers=headers, params=params)
        data_json = response.json()
        print(data_json)

        if 'data' not in data_json or 'children' not in data_json['data']:
            break

        posts = data_json['data']['children']
        all_posts.extend(posts)

        after = data_json['data'].get('after')
        if not after or len(all_posts) >= 1000:  # Stop after 1000 posts (or no more pages)
            break

    return all_posts

#----------------------------------------------
query = 'title:"this game is" OR title:"I love" OR title:"I hate" OR title:"I like" OR title:"Unpopular Opinion"'
ENDPOINT = 'https://oauth.reddit.com/r/Sims4/search/'

# Fetch posts for different sort types
top_posts = get_posts(ENDPOINT, query, 'top')
hot_posts = get_posts(ENDPOINT, query, 'hot')
new_posts = get_posts(ENDPOINT, query, 'new')

# Combine all posts into one list 
all_posts = top_posts + hot_posts + new_posts
    

#----------------------------------------------

# Now I want to place data into a pandas dataframe
# and combinine the dataframes into one


df = pd.DataFrame([{
    'subreddit': post['data']['subreddit'],
    'title': post['data']['title'],
    'selftext': post['data']['selftext'],
    'upvote_ratio': post['data']['upvote_ratio'],
    'ups': post['data']['ups'],
    'downs': post['data']['downs'],
    'score': post['data']['score']
} for post in all_posts])


#----------------------------------------------
# Importing into a streamlit so I
# can view the data better
st.title("Sims 4 Subreddit Data")
st.dataframe(df)


