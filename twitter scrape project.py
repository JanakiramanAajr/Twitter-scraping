# pip install snscrape
# pip install dnspython
# pip install pymongo[srv]
# pip install streamlit



import streamlit as st
import datetime
import snscrape.modules.twitter as sntwitter
import os
import pandas as pd
from datetime import date
import pymongo
from numpy import number
client = pymongo.MongoClient("mongodb+srv://ajr:1010@cluster0.qzzqxkq.mongodb.net/?retryWrites=true&w=majority",)
db = client.project
a=db.guviproject
# a.delete_many({})
st.title(f':blue[_Hello_]')
st.title(f'This is :red[TWITTER SCRAPING]')
st.write(f'In hear we gone _scrape_ the :red[_Tweets_] and downlode as we required')



search= st.text_input('Search')

st.write('Here we :red[search] :blue[_Tweet_] and :blue[_Hashtag_] ')

 
start_date = st.date_input(
    "Select Start Date",
datetime.date(2023, 2,25))
st.write('Here we :red[Select] :blue[_From date_] ')
end_date = st.date_input(
  "Select End Date",
datetime.date(2023, 2,25))
st.write('Here we :red[Select] :blue[_To date_] ')

num = st.slider('Select number of tweets', 1, 1000, 10)
st.write('Here we :red[Select] :blue[_Number of data_] ')

if st.button('Search'):
    for tweets,tweet in enumerate(sntwitter.TwitterSearchScraper('search since:start_date until:end_date').get_items()):
        if tweets > num:
            break #number of tweets you want to scrape
        else:
            tweets1= {'_id': tweet.id,'Date': tweet.date,'Content':tweet.content,'User':tweet.username,'Replay_count':tweet.replyCount,'Replay_RetweetCount':tweet.retweetCount,'Language':tweet.lang,'Source':tweet.source,'like_Count':tweet.likeCount,'url':tweet.url}
            a.insert_one(dict(tweets1))
            tweets+=1
    st.write('Here we :red[go] ')

df = pd.DataFrame(list(a.find()))
st.write('Here we :red[Select] :blue[_Display button_] to display data we searched ')
if st.button('display data'):
    @st.cache_data
    def load_data():
        return pd.DataFrame(df)
    st.checkbox("Use container width", value=False, key="use_container_width")
    df1=load_data()
    st.dataframe(df, use_container_width=st.session_state.use_container_width)
st.write('Here we need to :red[Download] select- :blue[_Download_] button')

if st.button('Download'):
    st.write('Here :blue[_For CSV_]')
    st.download_button('download csv',df.to_csv(),file_name='file.csv',mime='text/csv')

    st.write('Here :red[Json]')
    text_contents = df.to_json(default_handler=str).encode()
    st.download_button('Download as json', text_contents)








