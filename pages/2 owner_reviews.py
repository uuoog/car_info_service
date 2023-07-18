from wordcloud import WordCloud
import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
import time

df = pd.read_csv("./data/wordcloud2.csv")
scores = pd.read_csv("./data/owner_score_preprocessing.csv")

st.title('자동차 ')

car_options = df['name'].unique()
selected_cars = st.selectbox('자동차 선택', car_options)

filtered_df = df[df["name"].isin([selected_cars])]


content_values = filtered_df["content"].values

word_count = {}
for content in content_values:
    words = content.split()
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1

icon = Image.open("./img/car.png")
mask = Image.new("RGB", icon.size, (255,255,255))
mask.paste(icon,icon)
mask = np.array(mask)

wordcloud = WordCloud(font_path="./fonts/NanumGothicCoding.ttf", width=600, height=400, background_color='white',mask=mask,margin=2).generate_from_frequencies(word_count)

wordcloud_image =wordcloud.to_image()

with st.spinner("wordcloud를 구성 중 입니다."):
    time.sleep(3)
st.success('완료!')
st.image(wordcloud_image)

car_scores = scores[scores['name'] == selected_cars]
st.subheader('자동차 소유자 평가')
col1,col2,col3 = st.columns(3)

with col1:
    drivability_score = car_scores['driving'].values[0]
    price_score = car_scores['price'].values[0]
    st.write(f"주행: {car_scores['driving'].values[0]}")
    st.write(f"가격: {car_scores['price'].values[0]}")
with col2:
    habitability_score = car_scores['habitability'].values[0]
    quality_score = car_scores['quality'].values[0]
    st.write(f"거주성: {car_scores['habitability'].values[0]}")
    st.write(f"품질: {car_scores['quality'].values[0]}")
with col3:
    design_score = car_scores['design'].values[0]
    fuel_economy_score = car_scores['fuel_economy'].values[0]
    st.write(f"디자인: {car_scores['design'].values[0]}")
    st.write(f"연비: {car_scores['fuel_economy'].values[0]}")

total_score = (drivability_score + price_score
               + habitability_score + quality_score
               + design_score + fuel_economy_score) / 6


markdown_text = f"<p style='text-align: right; font-size: 24px;color:red;'>총점: {total_score:.1f}/10</p>"
st.markdown(markdown_text, unsafe_allow_html=True)

