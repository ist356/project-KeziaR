import pytest 
import pandas as pd
import sys
import os 
import code.Sentiment as sent

def test_sentiment():
    file = sent.CACHE_SENTIMENT_FILE

    lines = 51
    cols = [ c.strip().lower() for c in "title,sentence_text,sentence_sentiment,confidenceScores.positive,confidenceScores.neutral,confidenceScores.negative,upvote_ratio,ups".split(",")]

    print(f"TESTING: {file} file exists")
    assert os.path.exists(file)

    print(f"TESTING: {file} read_csv, {lines} lines")
    df = pd.read_csv(file)
    assert len(df) >=  lines
    
    print(f"TESTING: {file} columns : {cols}")
    for c in df:
        assert c.lower() in cols