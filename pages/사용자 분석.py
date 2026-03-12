import streamlit as st
import pandas as pd
import plotly.express as px

st.title("👤 User Activity Overview")

# ----------------------------
# 설명
# ----------------------------

st.markdown("""
### 사용자 활동 분석

이 페이지에서는 **TVING 사용자들의 기본적인 서비스 이용 패턴**을 분석합니다.

OTT 플랫폼에서는 사용자 행동 데이터가 다음과 같은 의사결정에 활용됩니다.

- 개인화 콘텐츠 추천
- 사용자 유지 전략
- churn 위험 예측

본 분석에서는 다음 **핵심 행동 지표**를 중심으로 사용자 활동을 분석합니다.

**주요 지표**

• 총 시청 시간 (Total Watch Time)  
• 콘텐츠 시청 횟수 (Watch Count)  
• 검색 활동 (Search Activity)
""")

st.divider()

# ----------------------------
# 데이터 로드
# ----------------------------

df = pd.read_csv("data/processed/feature_table.csv")

# ----------------------------
# Sidebar Filter
# ----------------------------

st.sidebar.header("User Filter")

min_watch = st.sidebar.slider(
    "Minimum Watch Time",
    0,
    int(df["total_watch_time"].max()),
    0
)

filtered_df = df[df["total_watch_time"] >= min_watch]

# ----------------------------
# KPI
# ----------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Users",
    len(filtered_df)
)

col2.metric(
    "Avg Watch Time",
    round(filtered_df["total_watch_time"].mean(),2)
)

col3.metric(
    "Avg Search Count",
    round(filtered_df["search_count"].mean(),2)
)

st.divider()

# ----------------------------
# Watch Time Distribution
# ----------------------------

st.subheader("📺 Watch Time Distribution")

st.markdown("""
사용자별 총 시청 시간 분포를 나타냅니다.

이 그래프를 통해 다음 사용자 유형을 확인할 수 있습니다.

- **Heavy User** : 높은 시청 시간을 가진 핵심 사용자  
- **Light User** : 시청 활동이 낮은 사용자

OTT 서비스에서는 **시청 시간이 높은 사용자가 서비스 유지율이 높은 경향**이 있습니다.
""")

fig = px.histogram(
    filtered_df,
    x="total_watch_time",
    nbins=30,
    color_discrete_sequence=["#636EFA"]
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ----------------------------
# Search Activity
# ----------------------------

st.subheader("🔎 Search Activity")

st.markdown("""
검색 활동은 사용자의 **콘텐츠 탐색 행동**을 나타냅니다.

검색 활동이 높은 사용자는

- 콘텐츠 관심도가 높은 사용자
- 추천 시스템 반응도가 높은 사용자

일 가능성이 높습니다.
""")

fig2 = px.histogram(
    filtered_df,
    x="search_count",
    nbins=20,
    color_discrete_sequence=["#EF553B"]
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ----------------------------
# User Segment
# ----------------------------

st.subheader("👥 User Segment")

st.markdown("""
시청 시간을 기준으로 사용자를 세 가지 그룹으로 분류합니다.

- Light User
- Medium User
- Heavy User
""")

filtered_df["segment"] = pd.qcut(
    filtered_df["total_watch_time"],
    q=3,
    labels=["Light User","Medium User","Heavy User"]
)

seg = filtered_df["segment"].value_counts().reset_index()

fig3 = px.pie(
    seg,
    names="segment",
    values="count",
    color_discrete_sequence=["#636EFA","#00CC96","#EF553B"]
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ----------------------------
# 데이터 미리보기
# ----------------------------

st.subheader("📄 Feature Data Preview")

st.markdown("""
Feature Engineering을 통해 생성된 사용자 행동 데이터 일부입니다.

이 데이터는 이후

- **Churn Risk Prediction**
- **Intervention Recommendation**

모델의 입력 데이터로 사용됩니다.
""")

st.dataframe(filtered_df.head(50))

st.divider()

# ----------------------------
# Insight
# ----------------------------

st.subheader("📊 Insight")

st.markdown("""
사용자 행동 데이터를 분석한 결과 다음과 같은 특징을 확인할 수 있습니다.

**1️⃣ 일부 Heavy User가 플랫폼 시청 시간을 대부분 차지**

**2️⃣ 검색 활동이 낮은 사용자 그룹 존재**

**3️⃣ 사용자 engagement 수준에 큰 차이가 존재**

이 분석 결과는 다음 단계인

- **Churn Risk Prediction**
- **Intervention Strategy**

분석의 기반 데이터로 활용됩니다.
""")