import requests
import folium
import streamlit as st
from streamlit_folium import st_folium


# Google Maps API 키
api_key = st.secrets["GOOGLE_KEY"]

# 검색할 장소명
place = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기도", "강원도", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]
place_name = st.selectbox('지역', place)
car_service = ['현대 자동차 대리점', '기아 자동차 대리점', '쉐보레 자동차 대리점', '르노코리아 자동차 대리점', 'kg 모빌리티 자동차 대리점']
selected_fuel_types = st.selectbox('대리점', car_service)

# Google Maps Places API 엔드포인트 URL
url = f'https://maps.googleapis.com/maps/api/place/textsearch/json'

# 요청 파라미터 설정
query = f'{place_name} {selected_fuel_types}'  # 장소명과 대리점명을 공백으로 구분하여 전달
params = {
    'query': query,
    'key': api_key,
}

# API 호출 및 응답 받기
response = requests.get(url, params=params)
data = response.json()

# 결과 확인
search_dict = {}
if data['status'] == 'OK':
    results = data['results']
    for result in results:
        name = result['name']
        location = result['geometry']['location']
        search_dict[name] = (location["lat"], location["lng"])

        print(f'장소명: {name}, 위도: {location["lat"]}, 경도: {location["lng"]}')
else:
    print('장소 검색에 실패했습니다.')

map_center = [list(search_dict.values())[0][0], list(search_dict.values())[0][1]]  # 지도 중심 좌표 (위도, 경도)

# 지도 생성
# map_center = [list(search_dict.values())[0][0], list(search_dict.values())[0][1]]  # 지도 중심 좌표 (위도, 경도)
map_zoom = 12  # 확대/축소 레벨 (0부터 높아질수록 확대)
map_osm = folium.Map(location=map_center, zoom_start=map_zoom)

# 장소에 마커 추가
for name, loc in search_dict.items():
    lat, lng = loc
    marker = folium.Marker(location=[lat, lng], tooltip=name)
    map_osm.add_child(marker)

st_data = st_folium(map_osm, width=725)