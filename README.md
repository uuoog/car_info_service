# 예산을 기반으로 한 자동차 추천&정보제공 서비스 개발


## 어떤 서비스 인가
신차 구매자의 조건에 맞는 자동차를 추천 및 자동차 오너들의 평가를 공유하여 선택에 도움을 주는 서비스

### 기능1. 추천 서비스
![image](https://github.com/uuoog/car_info_service/assets/131653525/26e34ded-766b-410f-9068-199572b2851c)

차량 유형, 연료 유형, 예산을 기반으로 조회하여 조건에 맞는 차량들을 추천합니다.

### 기능2. 자동차 비교
![image](https://github.com/uuoog/car_info_service/assets/131653525/4db50d73-2355-4fa1-ac77-7429d6955cac)

비교하고 싶은 차량을 2개 이상의 차량을 선택하여 2개 이상의 차량 정보를 같이 확인하여 비교할 수 있습니다.

### 기능3. 오너평가 리뷰 wordcloud, 점수
![image](https://github.com/uuoog/car_info_service/assets/131653525/390f12a4-a0dc-4968-895f-d391c9ef774e)

차량 별 실제 오너들의 리뷰 wordcloud 와 평가 점수를 평균 점수로 제공합니다.

### 기능4. 키워드를 통한 자동차 검색
![image](https://github.com/uuoog/car_info_service/assets/131653525/3defe045-def0-48a5-bd58-b2c2a35aa5e1)

오너평가 리뷰를 tf-idf구현체를 사용하여 벡터화해 키워드를 검색해 키워드와 유사한 차량들을 제공합니다.


### 기능5. 지역별 자동차 대리점 위치정보 제공
![image](https://github.com/uuoog/car_info_service/assets/131653525/00b9df82-3c5b-47d4-955b-5729d7b9f830)

원하는 지역과 자동차 브랜드를 입력하면 해당 지역의 대리점들의 위치 정보를 제공합니다.


## 데이터 셋
### 데이터 출처 및 라이브러리
- 자동차 데이터: 크롤링을 통해 자동차 정보/제원, 이미지 수집
- 실제 오너 평가 점수 & 리뷰: 크롤링을 통해 실제 오너들의 리뷰와 평가 점수 수집

### 사용 라이브러리
- Selenium
-	BeautifulSoup
-	Pandas
-	Matplotlib
-	Komoran
-	Google.cloud
-	scikit-learn
-	Supabase
-	folium
-	numpy
  ...

마치며, 본 프로젝트는 새 자동차를 구매하고자 하는 소비자를 위해 자동차의 정보를 제공하여 선택을 쉽게 할 수 있도록 하고자 개발을 시작했습니다.

