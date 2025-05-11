import pandas as pd
import streamlit as st
import requests
import config
import time

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

# def get_posts(ENDPOINT, sort):


#     query = ' title:"this game is" OR title:"I love" OR title:"I hate" OR title:"I like" OR title:"Unpopular Opinion" OR title:"best"\
#     OR title:"good" OR title:"bad" OR title:"bug" OR title:"regret" OR title:"error" OR title:"amazing" OR title:"worst"\
#     OR selftext:"I hate" OR selftext:"I love" OR selftext:"I like" OR selftext:"the worst" OR selftext:"regret" '

    
#     all_posts = []  
#     limit = 100
#     after_id = 't3_qlrl28'

#     # before_id = ''

#     params = {
#             'q': query,
#             'type': 'posts',
#             'restrict_sr': 'on',
#             'sort': sort,
#             't': 'all',
#             'limit': limit,
#             'after': after_id
#             # 'before': before_id
#         }


#     ENDPOINT = f"https://oauth.reddit.com/r/Sims4/search"

# #----------------------------------------------
#     # part about pagination that I will use to get more posts

#     while True:

#         params['after'] = after_id

#         response = requests.get(ENDPOINT, headers=headers, params=params)
#         data_json = response.json()        

        
#         if 'data' not in data_json or 'children' not in data_json['data']:
#             break

#         for items in data_json['data']['children']:
#             all_posts.extend(items)

#         after = data_json['data'].get('after')

#         if not after or len(all_posts) >= 500 :
#             break

#         time.sleep(2)

#     return all_posts

# # #----------------------------------------------

# url = f"https://oauth.reddit.com/r/Sims4/search"

#     # Fetch posts for different sort types
# top_posts = get_posts(url, 'top')
# # hot_posts = get_posts(url, 'hot')
# # new_posts = get_posts(url, 'new')

#     # Combine all posts into one list 
# allposts = top_posts 


# #----------------------------------------------



# # Now I want to place data into a pandas dataframe
# # and combinine the dataframes into one


# df = pd.DataFrame([{
#     'subreddit': post['data']['subreddit'],
#     'title': post['data']['title'],
#     'selftext': post['data']['selftext'],
#     'upvote_ratio': post['data']['upvote_ratio'],
#     'ups': post['data']['ups'],
#     'downs': post['data']['downs'],
#     'score': post['data']['score']
# } for post in allposts])


# # ----------------------------------------------
# # Importing into a streamlit so I
# # can view the data better


# st.title("Sims 4 Subreddit Data")

# df = df.to_csv("Sims4_data.txt", index=False, sep='\t', encoding= 'utf-16')


def get_posts(endpoint, sort, after=None, limit=100):

   
    params = {
            'q': query,
            'type': 'posts',
            'restrict_sr': 'on',
            'sort': sort,
            't': 'all',
            'limit': limit,
            'after': after
        }

    all_posts = []  

#----------------------------------------------
    # part about pagination that I will use to get more posts
    
    while True:

        params['after'] = after

        response = requests.get(endpoint, headers=headers, params=params, allow_redirects=False)
        data_json = response.json()

        if 'data' not in data_json or 'children' not in data_json['data']:
            break

        posts = data_json['data']['children']
        all_posts.extend(posts)

        after = data_json['data'].get('after')

        if not after or len(all_posts) >= 1000:
            break
        
        time.sleep(2)

    return all_posts

#----------------------------------------------
query = ' title:"this game is" OR title:"I love" OR title:"I hate" OR title:"I like" OR title:"Unpopular Opinion" OR title:"best"\
OR title:"good" OR title:"bad" OR title:"bug" OR title:"regret" OR title:"error" OR title:"amazing" OR title:"worst"\
OR selftext:"I hate" OR selftext:"I love" OR selftext:"I like" OR selftext:"the worst" OR selftext:"regret" '

endpoint = 'https://oauth.reddit.com/r/Sims4/search/'

# Combine all posts into one list 
top_posts = get_posts(endpoint, 'top')


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
} for post in top_posts])


#----------------------------------------------
# Importing into a streamlit so I
# can view the data better


#st.title("Sims 4 Subreddit Data")

df = df.to_csv("Sims4_data.txt", index=False, sep='\t', encoding= 'utf-16')

