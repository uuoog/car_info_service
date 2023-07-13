

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

df = pd.read_csv("./pages/wordcloud2.csv")

st.title('자동차 비교')

# 자동차 선택을 위한 드롭다운 메뉴 추가
car_options = df['name'].unique()
selected_cars = st.selectbox('자동차 선택', car_options)

# Step 1: Filter the DataFrame based on the condition


filtered_df = df[df["name"].isin([selected_cars])]

# Step 2: Retrieve the content values from the filtered DataFrame
content_values = filtered_df["content"].values

# Step 3: Process the content values to create a word frequency dictionary
word_count = {}
for content in content_values:
    words = content.split()  # Split the content into individual words
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1  # Count the frequency of each word

# Step 4: Generate the word cloud from the word frequency dictionary
wordcloud = WordCloud(font_path="C:/Windows/Fonts/malgun.ttf", width=800, height=400, background_color='white').generate_from_frequencies(word_count)

# Display the word cloud using streamlit
st.image(wordcloud.to_array())