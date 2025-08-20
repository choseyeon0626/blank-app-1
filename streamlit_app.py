# streamlit_app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- 핵심 기능 함수 ---

def get_zodiac_sign(month, day):
    """월과 일을 입력받아 해당하는 별자리를 문자열로 반환합니다."""
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "양자리"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "황소자리"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "쌍둥이자리"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "게자리"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "사자자리"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 23):
        return "처녀자리"
    elif (month == 9 and day >= 24) or (month == 10 and day <= 22):
        return "천칭자리"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 22):
        return "전갈자리"
    elif (month == 11 and day >= 23) or (month == 12 and day <= 24):
        return "사수자리"
    elif (month == 12 and day >= 25) or (month == 1 and day <= 19):
        return "염소자리"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "물병자리"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "물고기자리"
    return None

# st.cache_data: 함수의 실행 결과를 캐싱하여, 동일한 입력에 대해서는 다시 계산하지 않고 저장된 값을 반환합니다.
# ttl (time-to-live): 캐시의 유효 시간(초 단위)을 설정합니다. 6시간(21600초)으로 설정하여 불필요한 웹 요청을 줄입니다.
@st.cache_data(ttl=21600)
def get_todays_horoscope(zodiac_sign):
    """
    별자리 이름을 입력받아 네이버 운세 페이지에서 오늘의 운세를 스크레이핑하여 반환합니다.
    """
    try:
        # 네이버 검색 URL을 사용해 운세 정보 요청
        url = f"https://search.naver.com/search.naver?query={zodiac_sign}+운세"
        # 웹사이트가 자동화된 요청을 차단하는 것을 피하기 위해 User-Agent 헤더를 추가합니다.
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 요청이 실패하면 예외를 발생시킵니다.

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 운세 내용이 담긴 HTML 요소를 CSS 선택자로 찾습니다.
        # 주의: 이 선택자는 네이버 웹사이트의 구조가 변경되면 동작하지 않을 수 있습니다.
        horoscope_element = soup.select_one('div.detail > p.text')
        
        if horoscope_element:
            return horoscope_element.get_text(strip=True)
        else:
            return "운세 정보를 가져올 수 없습니다. 웹 페이지의 구조가 변경된 것 같습니다."
            
    except requests.exceptions.RequestException as e:
        return f"웹 페이지에 연결하는 중 오류가 발생했습니다: {e}"
    except Exception as e:
        return f"알 수 없는 오류가 발생했습니다: {e}"

# --- Streamlit UI 구성 ---

# 페이지 제목 설정
st.title("✨ 별자리 운세")

# 사용자로부터 생년월일 입력받기
# st.session_state를 사용하여 입력값을 세션 간에 유지할 수 있습니다.
if 'birth_input' not in st.session_state:
    st.session_state.birth_input = "08-14"

birth_input = st.text_input(
    label="생년월일을 입력하세요 (월-일 형식)",
    value=st.session_state.birth_input,
    placeholder="예시) 08-14",
    key="birth_input" # 입력 위젯의 상태를 세션 상태와 연결
)

# '운세 확인' 버튼
if st.button("오늘의 운세 확인하기"):
    if birth_input:
        try:
            # 입력된 문자열을 '-' 기준으로 나누어 월과 일로 변환
            month, day = map(int, birth_input.split('-'))
            
            # 별자리 계산
            zodiac_sign = get_zodiac_sign(month, day)
            
            if zodiac_sign:
                st.success(f"당신의 별자리는 **'{zodiac_sign}'** 입니다.")
                
                # 운세를 가져오는 동안 스피너(로딩 애니메이션) 표시
                with st.spinner(f"'{zodiac_sign}'의 오늘의 운세를 가져오는 중..."):
                    horoscope = get_todays_horoscope(zodiac_sign)
                    st.markdown("---")
                    st.subheader(f"오늘의 {zodiac_sign} 운세")
                    st.info(horoscope)
            else:
                st.error("유효하지 않은 날짜입니다. 다시 입력해주세요.")

        except ValueError:
            st.error("입력 형식이 잘못되었습니다. '월-일' 형식으로 입력해주세요. (예: 08-14)")
        except Exception as e:
            st.error(f"처리 중 오류가 발생했습니다: {e}")
    else:
        st.warning("생년월일을 입력해주세요.")