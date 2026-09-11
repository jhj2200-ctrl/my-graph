import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    
    # 날짜 열을 datetime 형식으로 변환 (YYYYMMDD 형식 처리)
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
# [구역 1] 영화별 일관객 변화 (단일 선 그래프)
# -----------------------------------------------------------------------------
st.header("1. 개별 영화 날짜별 일관객 추이")

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

# 플롯리 선 그래프 생성
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
# [구역 2] 일관객 합계 상위 5개 영화 추이 비교 (다중 선 그래프)
# -----------------------------------------------------------------------------
st.header("2. 일관객 합계 상위 5개 영화 비교")

# 일관객 합계 상위 5개 영화 추출
top5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index.tolist()

# 상위 5개 영화 데이터 필터링
top5_df = df[df['영화명'].isin(top5_movies)].sort_values('날짜')

# 플롯리 다중 선 그래프 생성
fig2 = px.line(
    top5_df,
    x='날짜',
    y='일관객',
    color='영화명',
    title="일관객 합계 상위 5개 영화의 날짜별 일관객 추이 비교",
    labels={'날짜': '날짜', '일관객': '일관객 수(명)', '영화명': '영화 제목'},
    markers=True
)

fig2.update_traces(
    hovertemplate="<b>영화:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",
    legend_title_text="영화 제목 (클릭 시 켜기/끄기)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 인사이트 문구 자리
top5_names_str = ", ".join(top5_movies)
st.info(f"💡 **이 그래프로 알 수 있는 것:** 전체 기간 관객 동원력 상위 5개 영화({top5_names_str})의 개봉 시기별 일관객 스파이크 지점과 흥행 경쟁 구도를 한눈에 비교할 수 있습니다.")

st.divider()

# -----------------------------------------------------------------------------
# [구역 3] 날짜별 TOP 10 총 관객수 영역 그래프
# -----------------------------------------------------------------------------
st.header("3. 날짜별 TOP 10 총 관객수 추이")

# 날짜별 일관객 합계 계산
daily_total = df.groupby('날짜')['일관객'].sum().reset_index().sort_values('날짜')

# 관객수 합계 상위 3일 추출
top3_days = daily_total.nlargest(3, '일관객')

# 영역 그래프 생성 (px.area)
fig3 = px.area(
    daily_total,
    x='날짜',
    y='일관객',
    title="날짜별 박스오피스 TOP 10 총 관객수 추이 (최대 관객 3일 표시)",
    labels={'날짜': '날짜', '일관객': '총 관객수(명)'}
)

fig3.update_traces(
    line_color='#1f77b4',
    fillcolor='rgba(31, 119, 180, 0.3)',
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>총 관객수:</b> %{y:,}명<extra></extra>"
)

# 관객수 TOP 3 날짜를 그래프 상에 포인트 및 라벨(주석)로 표시
for rank, (_, row) in enumerate(top3_days.iterrows(), 1):
    day_str = row['날짜'].strftime('%Y-%m-%d')
    val = row['일관객']
    
    # 상위 3일 포인트 표시
    fig3.add_trace(go.Scatter(
        x=[row['날짜']],
        y=[val],
        mode='markers+text',
        marker=dict(color='red', size=10, symbol='circle'),
        text=[f" 🏆 TOP {rank}<br> ({day_str})"],
        textposition="top center",
        name=f"TOP {rank}: {day_str}",
        showlegend=False,
        hovertemplate=f"<b>TOP {rank} 관객수 최고일</b><br>날짜: {day_str}<br>총 관객수: {val:,}명<extra></extra>"
    ))

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="총 관객수 (명)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig3, use_container_width=True)

# TOP 3 날짜 정보를 인사이트 문구에 활용
top3_str_list = [f"{row['날짜'].strftime('%Y년 %m월 %d일')}({row['일관객']:,}명)" for _, row in top3_days.iterrows()]
st.info(f"💡 **이 그래프로 알 수 있는 것:** 1년 중 박스오피스 전체 관객 수가 가장 몰렸던 극장가 최고 성수기 Top 3날짜인 **{top3_str_list[0]}**, **{top3_str_list[1]}**, **{top3_str_list[2]}**를 직관적으로 확인할 수 있습니다.")

st.divider()

# -----------------------------------------------------------------------------
# [구역 4] 전체 기간 일관객 합계 TOP 10 (가로 막대그래프)
# -----------------------------------------------------------------------------
st.header("4. 전체 기간 총 관객수 TOP 10 영화")

# 영화별 일관객 합계 및 10위권 진입 일수 계산
top10_movies_df = df.groupby('영화명').agg(
    총관객수=('일관객', 'sum'),
    차트진입일수=('날짜', 'count')
).reset_index()

# 총관객수 기준 상위 10개 영화 추출 (내림차순 정렬)
top10_movies_df = top10_movies_df.sort_values('총관객수', ascending=True).tail(10)

# 가로 막대그래프 생성 (px.bar)
fig4 = px.bar(
    top10_movies_df,
    x='총관객수',
    y='영화명',
    orientation='h',
    title="전체 기간 일관객 합계 TOP 10 영화 (10위권 진입 일수 포함)",
    labels={'총관객수': '총 관객수(명)', '영화명': '영화 제목', '차트진입일수': '10위권 진입 일수'},
    hover_data={'총관객수': ':,d', '차트진입일수': True},
    color='총관객수',
    color_continuous_scale='Blues'
)

fig4.update_traces(
    hovertemplate="<b>영화명:</b> %{y}<br><b>총 관객수:</b> %{x:,}명<br><b>10위권 진입 일수:</b> %{customdata[0]}일<extra></extra>",
    customdata=top10_movies_df[['차트진입일수']]
)

fig4.update_layout(
    xaxis_title="총 관객수 (명)",
    yaxis_title="영화 제목",
    coloraxis_showscale=False,
    template="plotly_white"
)

st.plotly_chart(fig4, use_container_width=True)

# 인사이트 문구
top1_movie = top10_movies_df.iloc[-1]
st.info(f"💡 **이 그래프로 알 수 있는 것:** 1위인 **'{top1_movie['영화명']}'**({top1_movie['총관객수']:,}명, {top1_movie['차트진입일수']}일간 10위권 유지)를 비롯해, 관객수 상위 10개 영화의 전체 관객 동원력 및 박스오피스 상위권 장기 집권(10위권 진입 일수) 정도를 한눈에 파악할 수 있습니다.")

st.divider()

# -----------------------------------------------------------------------------
# [구역 5] 월 × 요일별 일관객 합계 (히트맵)
# -----------------------------------------------------------------------------
st.header("5. 월 × 요일별 관객수 분포 히트맵")

# 데이터 복사 후 월, 요일 컬럼 추출
df_heatmap = df.copy()
df_heatmap['월'] = df_heatmap['날짜'].dt.month.map(lambda x: f"{x}월")
df_heatmap['요일'] = df_heatmap['날짜'].dt.day_name()

# 요일 한글 변환 매핑
days_ko = {
    'Monday': '월요일',
    'Tuesday': '화요일',
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}
df_heatmap['요일'] = df_heatmap['요일'].map(days_ko)

# 정렬용 카테고리 설정 (월~일 순서 지정)
days_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
months_order = [f"{m}월" for m in range(1, 13)]

# 월 x 요일 그룹화 및 피벗 테이블 작성
heatmap_pivot = df_heatmap.groupby(['월', '요일'])['일관객'].sum().reset_index()

# Categorical 변환을 통해 지정한 순서대로 정렬
heatmap_pivot['월'] = pd.Categorical(heatmap_pivot['월'], categories=months_order, ordered=True)
heatmap_pivot['요일'] = pd.Categorical(heatmap_pivot['요일'], categories=days_order, ordered=True)
heatmap_matrix = heatmap_pivot.pivot(index='월', columns='요일', values='일관객').fillna(0)

# 히트맵 생성 (px.imshow)
fig5 = px.imshow(
    heatmap_matrix,
    labels=dict(x="요일", y="월", color="총 관객수(명)"),
    x=days_order,
    y=[m for m in months_order if m in heatmap_matrix.index],
    color_continuous_scale="YlOrRd",
    title="월 × 요일별 박스오피스 일관객 합계 히트맵"
)

fig5.update_traces(
    hovertemplate="<b>%{y} %{x}</b><br>총 관객수: %{z:,}명<extra></extra>"
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    template="plotly_white"
)

st.plotly_chart(fig5, use_container_width=True)

# 인사이트 문구
st.info("💡 **이 그래프로 알 수 있는 것:** 연중 어떤 월의 어떤 요일(예: 주말 또는 특정 명절/휴가철 달)에 관객 몰림 현상이 집중되는지 색상의 짙은 정도를 통해 계절성 및 요일별 특성을 즉시 직관적으로 비교할 수 있습니다.")

st.divider()

# -----------------------------------------------------------------------------
# [구역 6] 추후 그래프 추가 구역 (확장용)
# -----------------------------------------------------------------------------
st.header("6. 추가 시계열 분석 (예정)")
st.caption("새로운 분석 그래프가 이 구역에 지속적으로 추가될 예정입니다.")

with st.expander("📌 앞으로 추가할 수 있는 아이디어 예시"):
    st.write("- **상위 N개 영화의 누적관객 비교 선 그래프**")
    st.write("- **스크린 수 및 상영횟수 대비 일관객 비중 추이**")
