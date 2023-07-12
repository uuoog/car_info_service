
import streamlit as st
from google.cloud import bigquery

client = bigquery.Client.from_service_account_json(r'C:/Users/kdaj8/.ssh/weekly_pj/eng-copilot-392105-769b6f2fe797.json')
query = f"""
SELECT *
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
st.sidebar.markdown("## 차량 검색")
search_query = st.sidebar.text_input("", max_chars=50)
search_button = st.sidebar.button("검색")


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
    st.write(f"연비: {car['km_l']}")
    st.write(f"차량 유형: {car['Size']} {car['Type']}")
    st.write(f"배기량: {car['cc']}")



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

        st.header('추천 차량')
        #st.table(recommended_cars)
        if recommended_cars.empty:
            st.write('선택한 유형과 가격대에 해당하는 차량이 없습니다.')
        else:
            st.write('선택한 유형과 가격대에 대한 추천 차량 목록입니다:')
            col1, col2 = st.columns(2)
            for i in range(0, len(recommended_cars), 2):
                with col1:
                    if i < len(recommended_cars):
                        car1 = recommended_cars.iloc[i]
                        st.subheader(car1['name'])
                        st.image(car1['img'])
                        st.write(f"연료 종류: {car1['fuel_kind']}")
                        st.write(f"가격: {car1['min_price']}~{car1['max_price']} 만 원")
                        st.write(f"연비: {car1['km_l']}")
                        st.write(f"차량 유형: {car1['Size']} {car1['Type']}")
                        st.write(f"배기량: {car1['cc']}")
                with col2:
                    if i + 1 < len(recommended_cars):
                        car2 = recommended_cars.iloc[i + 1]
                        st.subheader(car2['name'])
                        st.image(car2['img'])
                        st.write(f"연료 종류: {car2['fuel_kind']}")
                        st.write(f"가격: {car2['min_price']}~{car2['max_price']} 만 원")
                        st.write(f"연비: {car2['km_l']}")
                        st.write(f"차량 유형: {car2['Size']} {car2['Type']}")
                        st.write(f"배기량: {car2['cc']}")

else:
    st.warning('예산을 입력해주세요.')





if search_button:
    matching_cars = df[df['name'].str.contains(search_query, case=False)]
    if not matching_cars.empty:
        for index, car in matching_cars.iterrows():
            display_car_information(car)
    else:
        st.write("일치하는 차량이 없습니다.")