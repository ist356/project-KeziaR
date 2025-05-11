import requests
from Api_calls import headers
from Api_calls import TOKEN_ACCESS

# def make_reddit_api_request(TOKEN_ACCESS, headers):
#     response = requests.get(TOKEN_ACCESS, headers=headers)
    
#     # Check for rate limit headers
#     used = response.headers.get('X-Ratelimit-Used')
#     remaining = response.headers.get('X-Ratelimit-Remaining')
#     reset = response.headers.get('X-Ratelimit-Reset')
    
#     print(f"X-Ratelimit-Used: {used}")
#     print(f"X-Ratelimit-Remaining: {remaining}")
#     print(f"X-Ratelimit-Reset: {reset}")
    
#     return response


# TOKEN_ACCESS = 'https://www.reddit.com/api/v1/access_token'
# headers = {
#     'Authorization': 'bearer {TOKEN}',
#     'User-Agent': 'MyAPI/0.0.1',

#     }

# response = make_reddit_api_request(TOKEN_ACCESS, headers)



