from konlpy.tag import Komoran
import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties
import re

credentials = service_account.Credentials.from_service_account_info(
    st.secrets['gcp_service_account']
)
client = bigquery.Client(credentials=credentials)
# client = bigquery.Client.from_service_account_json(r'./data/eng-copilot-392105-769b6f2fe797.json')

query = f"""
SELECT *, REPLACE(km_l, "~", "-") as r_km_l, REPLACE(cc, "~", "-") as r_cc

FROM
	`eng-copilot-392105.Dataset.car_by_price_fuel`
JOIN
	`eng-copilot-392105.Dataset.domestic_car_img`
ON
	`eng-copilot-392105.Dataset.car_by_price_fuel`.name = `eng-copilot-392105.Dataset.domestic_car_img`.name;

"""
query_job = client.query(query)
#데이터프레임으로 변환
df = query_job.to_dataframe()
tk = pd.read_csv("data/owner_reviews_tokenized.csv")
st.sidebar.markdown("## 차량 검색")
search_query = st.sidebar.selectbox("차량을 선택해주세요",df["name"])
search_button = st.sidebar.button("검색")


#자동차 추천기능
with st.form("my car"):
    st.title('차량 추천 서비스')
    selected_type = st.selectbox('차량 유형 선택', df['Type'].unique())
    fuel_kind = ['가솔린', '디젤', 'LPG', '하이브리드', '전기', '수소']
    selected_fuel_types = st.multiselect('차량 연료 유형 선택', fuel_kind)
    budget = st.text_input('예산을 입력하세요', value='', placeholder='단위: 만 원')
    submitted = st.form_submit_button("검색")

def display_car_information(car):
    st.subheader(car['name'])
    st.image(car['img'])
    st.write(f"연료 종류: {car['fuel_kind']}")
    st.write(f"가격: {car['min_price']}~{car['max_price']} 만원")
    st.write(f"연비: {car['r_km_l']}")
    st.write(f"차량 유형: {car['Size']} {car['Type']}")
    st.write(f"배기량: {car['r_cc']}")

def extract_minimum_value(text):
    pattern = r'\d+(.\d+)?' # 소수점 문자를 찾기위해 ?는 0번째 또는 1번째 나타나는 숫자
    match = re.search(pattern, text)  # 패턴과 일치하는 첫 번째 숫자를 찾음
    if match:
        return float(match.group())
    else:
        return None

if budget:
    try:
        budget = int(budget)
    except ValueError:
        st.warning('유효한 숫자를 입력해주세요.')
    else:

        recommended_cars = df[

            (df['fuel_gas'].isin(selected_fuel_types) |
             df['fuel_die'].isin(selected_fuel_types) |
             df['fuel_lpg'].isin(selected_fuel_types) |
             df['fuel_hyb'].isin(selected_fuel_types) |
             df['fuel_ele'].isin(selected_fuel_types) |
             df['fuel_hyd'].isin(selected_fuel_types)) &
            (df['Type'] == selected_type)
            &(df['min_price'] <= budget) & (df['max_price'] >= budget)]

        recommended_cars['composite_fuel_economy'] = recommended_cars['km_l'].apply(extract_minimum_value)

        st.header('추천 차량')
        #st.table(recommended_cars)
        if recommended_cars.empty:
            st.write('선택한 유형과 가격대에 해당하는 차량이 없습니다.')
        else:
            st.write('선택한 유형과 가격대에 대한 추천 차량 목록입니다:')
            col1, col2 = st.columns(2)
            for i in range(0, len(recommended_cars), 2):
                with col1:
                    car1 = recommended_cars.iloc[i]
                    display_car_information(car1)
                with col2:
                    if i + 1 < len(recommended_cars):
                        car2 = recommended_cars.iloc[i + 1]
                        display_car_information(car2)

        if not recommended_cars.empty:
            st.markdown("예산에 맞춰진 차량의 연비 경제성 비교입니다.")


            font_dirs = ['./fonts']
            font_files = fm.findSystemFonts(fontpaths=font_dirs)

            for font_file in font_files:
                fm.fontManager.addfont(font_file)
            fm._load_fontmanager(try_read_cache=False)
            plt.rcParams['font.family'] = 'NanumGothicCoding'


            sorted_cars = recommended_cars.sort_values('composite_fuel_economy')
            fuel_economy_values = sorted_cars['composite_fuel_economy'].tolist()
            fig, ax = plt.subplots()
            ax.barh(sorted_cars['name'], fuel_economy_values)
            for i, v in enumerate(fuel_economy_values):
                ax.text(v + 0.1, i, str(v), color='black', ha='left', va='center')
            plt.title('추천 차량의 연비 경제성')
            plt.xlabel('연비 (km/l)')
            plt.ylabel('차량')
            st.pyplot(fig)

else:
    st.warning('예산을 입력해주세요.')




#자동차 비교
def main():
    st.title('자동차 비교')

    # 자동차 선택을 위한 드롭다운 메뉴 추가
    car_options = df['name'].unique()
    selected_cars = st.multiselect('비교할 자동차 선택', car_options)

    if len(selected_cars) != 2:
        st.warning('비교할 자동차를 2개  선택해주세요.')
    else:


        car1 = selected_cars[0]
        car2 = selected_cars[1]
        col1, col2 = st.columns(2)

        with col1:
            display_car_information(df[df['name'] == car1].iloc[0])
        with col2:
            display_car_information(df[df['name'] == car2].iloc[0])

if __name__ == "__main__":
    main()

#### 키워드 검색 구현기능

komoran = Komoran(userdic="./data/user.dic")
tk["contents_tokens"] = tk["content_tokens"].apply(lambda x: eval(x))

def extract_nouns(tokens):
    return [text for text, tag in tokens if tag in ("NNP", "NNG")]

tk["content_nouns"] = tk["contents_tokens"].apply(lambda x: extract_nouns(x))
# Sklearn 이용 TfidfVectorizer 사용

def dummy_fun(doc):
    return doc

tfidf = TfidfVectorizer(
    analyzer='word',
    tokenizer=dummy_fun,
    preprocessor=dummy_fun,
    token_pattern=None
)

tfidf_csr_matrix = tfidf.fit_transform(tk["content_nouns"])

def tokenize(text):
    tokens = komoran.pos(text)
    nouns = [text for text, tag in tokens if tag in ("NNP", "NNG")]
    return nouns


@st.cache_data
def search(query, k=5):
    query_tokens = tokenize(query)
    query_tfidf = tfidf.transform([query_tokens])
    similarities = cosine_similarity(query_tfidf, tfidf_csr_matrix).flatten()
    top_similarities = sorted(similarities)[-k:][::-1]
    top_indices = similarities.argsort()[-k:][::-1]
    top_titles = [tk.iloc[i]["name"] for i in top_indices]
    return top_titles



st.title("키워드를 통한 자동차 검색")
query = st.text_input("검색어를 입력하세요.")
if st.button("Search") :
     top_titles = search(query)
     for  title in top_titles:
         st.write(title)

if search_button:
    matching_cars = df[df['name'].str.contains(search_query, case=False)]
    if not matching_cars.empty:
        for index, car in matching_cars.iterrows():
            display_car_information(car)
    else:
        st.write("일치하는 차량이 없습니다.")
