import streamlit as st
from supabase import create_client

# Supabase 정보
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase_client = init_connection()

# Streamlit 애플리케이션 시작
st.title('서비스에 대한 평가를 해주세요.')

# 사용자 입력 받기
feedback = st.text_area("", placeholder="평가 내용")

def run_query(feedback):
    response = supabase_client.table("feedback").insert(
        {
            "feedback": feedback
        }
    ).execute()


if st.button("Submit"):
    # 사용자가 "Submit" 버튼을 클릭하면 피드백을 삽입하는 쿼리 실행
    result = run_query(feedback)
    st.success("피드백이 성공적으로 저장되었습니다!")