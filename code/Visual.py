import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import pandas as pd



# I need a plot that will show the difference between positive, neutral, and negative sentiment
# Loading data
pengo = pd.read_csv("df_best.csv")
pengo['count'] = 1

# barplot
figure, series1 = plt.subplots()
bar = sns.barplot(data=pengo, x="sentence_sentiment", y='max_confidence_score', hue= "sentence_sentiment", estimator="sum").set_title("Sentiment Analysis of Sims 4 Subreddit")


#----------------------------------------------
# I need a word cloud that will show the most common words in the selftext

# positive word cloud

pos_words = pengo[pengo['sentence_sentiment'] == 'positive']
pos_cloud = WordCloud(width=3000, height=1000, background_color='white', stopwords=STOPWORDS).generate(' '.join(pos_words['sentence_text']))
figure2 = plt.figure()
plt.title('Positive Sentiment')
plt.imshow(pos_cloud, interpolation="bilinear")
plt.axis("off")


# negative word cloud

neg_words = pengo[pengo['sentence_sentiment'] == 'negative']
neg_cloud = WordCloud(width=3000, height=1000, background_color='white', stopwords=STOPWORDS).generate(' '.join(neg_words['sentence_text']))
figure3 = plt.figure()
plt.title('Negative Sentiment')
plt.imshow(neg_cloud, interpolation="bilinear")
plt.axis("off")


# neutral word cloud

neutral_words = pengo[pengo['sentence_sentiment'] == 'neutral']
neutral_cloud = WordCloud(width=3000, height=1000, background_color='white', stopwords=STOPWORDS).generate(' '.join(neutral_words['sentence_text']))
figure4 = plt.figure()
plt.title('Nuetral Sentiment')
plt.imshow(neutral_cloud, interpolation="bilinear")
plt.axis("off")


#----------------------------------------------

# I want to have a sidebar that shows plots
st.sidebar.title("Plots")
#barplot
with st.sidebar:
    # Display the plot in Streamlit
    st.pyplot(figure)
#wordplots
    st.pyplot(figure2)
    st.pyplot(figure3)
    st.pyplot(figure4)

# I want a main section that shows and allows for the dataframe to be downloaded
st.title("Sims 4 Subreddit Data")
st.dataframe(pengo)
csv = pengo.to_csv(index=False).encode('utf-8')
st.download_button(label="Download CSV file", data=csv, file_name='sims4_sentiment_data.csv', mime='text/csv',
)