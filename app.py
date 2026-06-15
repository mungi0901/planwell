# =========================================================
# Project Title: Planwell (AI 기반 맞춤형 헬스케어 및 스케줄링 시스템)
# Student No, Name, E-mail: 22212076, 정문기, mungi00000@gmail.com
# Project Link: https://github.com/mungi0901/planwell
# =========================================================
import streamlit as st
import time
import random

# 1. Entity (Model) Layer
class Exercise:
    def __init__(self, name, sets, weight):
        self.name = name
        self.sets = sets
        self.weight = weight

class Routine:
    def __init__(self, routine_id, target_muscle, exercises, is_indoor):
        self.routine_id = routine_id
        self.target_muscle = target_muscle
        self.exercises = exercises
        self.is_indoor = is_indoor

# 2. Service Layer (기기 센서 및 외부 API 모방)
class HealthDataService:
    def get_data(self):
        time.sleep(0.5) # 블루투스 동기화 딜레이 모방
        return round(random.uniform(4.0, 8.5), 1), random.randint(60, 120)

class WeatherService:
    def get_weather(self):
        time.sleep(0.5) # API 네트워크 통신 모방
        return random.choices(["Clear", "Rain", "Fine Dust"], weights=[50, 30, 20])[0]

class AIEngineClient:
    def request_routine(self, sleep, hr, weather):
        time.sleep(1.0) # AI 연산 모방
        is_bad_weather = weather in ["Rain", "Fine Dust"]
        
        # 상태에 따른 AI 루틴 분기
        if is_bad_weather or sleep < 5.0 or hr > 100:
            exercises = [Exercise("폼롤러 전신 이완", 3, 0), Exercise("코어 플랭크", 3, 0), Exercise("실내 사이클", 1, 0)]
            return Routine("RTN-SUB", "전신 회복 (실내)", exercises, True)
        else:
            exercises = [Exercise("바벨 스쿼트", 5, 80), Exercise("레그 프레스", 4, 100), Exercise("야외 러닝", 1, 0)]
            return Routine("RTN-MAIN", "하체 및 유산소", exercises, False)

# 3. Repository Layer (데이터 총괄)
class RoutineRepository:
    def __init__(self):
        self.health = HealthDataService()
        self.weather = WeatherService()
        self.ai = AIEngineClient()

    def fetch_routine(self):
        sleep, hr = self.health.get_data()
        weather = self.weather.get_weather()
        routine = self.ai.request_routine(sleep, hr, weather)
        return routine, sleep, hr, weather

# 4. ViewModel Layer (MVVM 비즈니스 로직)
class RoutineViewModel:
    def __init__(self):
        self.repo = RoutineRepository()

    def generate_routine(self):
        routine, sleep, hr, weather = self.repo.fetch_routine()
        alert = None
        
        # State Machine Diagram 전이 로직 (경고 팝업)
        if weather in ["Rain", "Fine Dust"]:
            alert = f"기상 악화({weather})로 부상 위험이 있어 실내 루틴으로 대체됩니다."
        elif sleep < 5.0 or hr > 100:
            alert = f"컨디션 저하(수면 {sleep}h, 심박수 {hr}bpm)가 감지되어 회복 루틴이 제공됩니다."
            
        return routine, alert, sleep, hr, weather

# 5. View Layer (모바일 웹 화면 UI)
def main():
    # 모바일 앱 느낌을 주기 위한 페이지 중앙 정렬 설정
    st.set_page_config(page_title="Planwell", page_icon="📱", layout="centered")

    # 헤더 (앱 상단바 느낌)
    st.markdown("<h2 style='text-align: center; color: #2980B9;'>📱 Planwell</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>AI 맞춤형 헬스케어 시스템</p>", unsafe_allow_html=True)
    st.divider()

    # 메인 동작 버튼
    if st.button("오늘의 맞춤형 루틴 생성하기", type="primary", use_container_width=True):
        vm = RoutineViewModel()

        # 시퀀스 다이어그램 진행 상태 표시
        with st.spinner("스마트워치 데이터 동기화 및 AI 분석 중..."):
            routine, alert, sleep, hr, weather = vm.generate_routine()

        # 수집된 센서 데이터 대시보드
        st.subheader("실시간 컨디션 데이터")
        cols = st.columns(3)
        cols[0].metric("수면 시간", f"{sleep} h")
        cols[1].metric("현재 심박수", f"{hr} bpm")
        cols[2].metric("현재 날씨", weather)

        # 상태(State)에 따른 경고 알림 인터럽트
        if alert:
            st.warning(f"🚨[컨디션 경고] {alert}")
        else:
            st.success("컨디션이 최상입니다! 성장을 위한 고강도 루틴을 제공합니다.")

        # 루틴 결과 출력부 (Data Binding)
        st.subheader("추천 운동 스케줄")
        st.info(f"**타겟 부위:** {routine.target_muscle} \n\n **루틴 ID:** {routine.routine_id}")
        
        for idx, ex in enumerate(routine.exercises, 1):
            weight_str = f"{ex.weight}kg" if ex.weight > 0 else "맨몸"
            st.write(f"**{idx}. {ex.name}**")
            st.caption(f"↳ {ex.sets}세트 진행 | 중량: {weight_str}")
            
    st.divider()
    st.caption("© 2026 Planwell Project. All rights reserved.")

if __name__ == "__main__":
    main()