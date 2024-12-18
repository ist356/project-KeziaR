import requests 
import code.Api_calls as calls

def test_api():
    tests = {
        {'selftext': 'This is a terrible test post!', 'expected_sentiment': 'negative'},
        {'selftext': 'This test post is the best thing I have ever seen!', 'expected_sentiment': 'positive'}
    }
    for t in tests:
        print(f"\nTESTING: test_get_azure_sentiment({t['selftext']}) == {t['expected_sentiment']}")
        results = calls.get_azure_sentiment(t['selftext'])
        sentiment = results['results']['documents'][0]['sentiment']
        assert t['expected_sentiment'] == sentiment