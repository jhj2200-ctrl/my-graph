import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 데이터 로드 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 datetime 형식으로 변환 (YYYYMMDD)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치(365일) 일별 박스오피스 데이터를 바탕으로 시계열 흐름과 변화를 시각화합니다.")
st.divider()

# -----------------------------------------------------------------------------
# [구역 1] 영화별 일관객 변화 (선 그래프)
# -----------------------------------------------------------------------------
st.header("1. 영화별 일관객 추이 분석")

# 영화 목록 추출 (영화명 기준 정렬)
movie_list = sorted(df['영화명'].unique())

# 영화 선택 드롭다운
selected_movie = st.selectbox(
    "📊 분석할 영화를 선택하세요:",
    options=movie_list,
    index=0
)

# 선택된 영화 데이터 필터링 (날짜순 정렬)
movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

# Plotly 선 그래프 생성
fig1 = px.line(
    movie_df,
    x='날짜',
    y='일관객',
    title=f"'{selected_movie}' 날짜별 일관객 변화",
    labels={'날짜': '날짜', '일관객': '일관객 수(명)'},
    markers=True
)

fig1.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>"
)

fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 인사이트 문구 자리
st.info(f"💡 **이 그래프로 알 수 있는 것:** '{selected_movie}'의 상영 기간 동안 개봉 초기 화제성과 주말/평일 관객 수 추이 및 흥행 감소 흐름을 직관적으로 파악할 수 있습니다.")

st.divider()

# -----------------------------------------------------------------------------
# [구역 2] 추후 그래프 추가 구역 (확장용)
# -----------------------------------------------------------------------------
st.header("2. 추가 시계열 분석 (예정)")
st.caption("새로운 분석 그래프가 이 구역에 지속적으로 추가될 예정입니다.")

with st.expander("📌 앞으로 추가할 수 있는 아이디어 예시"):
    st.write("- **상위 N개 영화의 누적관객 비교 선 그래프**")
    st.write("- **월별 / 요일별 관객수 분포 히트맵**")
    st.write("- **스크린 수 및 상영횟수 대비 일관객 비중 추이**")
