import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("📺 TVING Service Dashboard")

st.markdown("""
TVING 플랫폼의 **사용자 행동 데이터를 기반으로 서비스 이용 패턴을 분석하는 대시보드**입니다.

이 페이지에서는 다음을 분석합니다.

- 플랫폼 전체 이용 규모
- 사용자 시청 패턴
- 검색 활동 분석
- 사용자 engagement 수준
""")

st.divider()

# -------------------------------------------------
# 데이터 로드
# -------------------------------------------------

@st.cache_data
def load_data():

    path = "data/processed/feature_table.csv"

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


df = load_data()

if df.empty:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()

# -------------------------------------------------
# 컬럼 자동 탐색
# -------------------------------------------------

def find_column(keywords):

    for col in df.columns:
        name = col.lower()

        for key in keywords:
            if key in name:
                return col

    return None


user_col = find_column(["user"])
watch_col = find_column(["watch","time"])
search_col = find_column(["search"])

# -------------------------------------------------
# Platform Overview
# -------------------------------------------------

st.subheader("📊 Platform Overview")

st.markdown("""
플랫폼의 **전체 이용 규모를 확인하기 위한 핵심 지표(KPI)** 입니다.

이 지표를 통해 다음을 파악할 수 있습니다.

- 플랫폼을 사용하는 **전체 사용자 규모**
- 수집된 **사용자 활동 데이터 양**
- 전체 서비스 이용 시간

이는 **플랫폼 engagement 수준을 이해하는 기준 지표**로 활용됩니다.
""")

col1, col2, col3 = st.columns(3)

total_users = df[user_col].nunique() if user_col else len(df)
total_rows = len(df)
total_watch = int(df[watch_col].sum()) if watch_col else 0

col1.metric("Total Users", total_users)
col2.metric("Total Records", total_rows)
col3.metric("Total Watch Time", total_watch)

st.divider()

# -------------------------------------------------
# Watch Time Distribution
# -------------------------------------------------

if watch_col:

    st.subheader("⏱ Watch Time Distribution")

    st.markdown("""
이 그래프는 **사용자 시청 시간의 분포를 분석하기 위한 히스토그램입니다.**

히스토그램을 사용하는 이유:

- 사용자 활동 데이터의 **분포 형태 확인**
- **Heavy User vs Light User 비율 파악**
- 플랫폼 engagement 수준 분석

분석 포인트:

- 시청 시간이 낮은 사용자 비율이 높으면 **light user 중심 플랫폼**
- 일부 사용자가 매우 높은 시청 시간을 가지면 **heavy user 존재**

이 분석은 **사용자 engagement 전략 및 retention 전략 수립에 중요합니다.**
""")

    fig = px.histogram(
        df,
        x=watch_col,
        nbins=30,
        labels={watch_col:"Watch Time"}
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------
# Search Activity Distribution
# -------------------------------------------------

if search_col:

    st.subheader("🔎 Search Activity Distribution")

    st.markdown("""
이 그래프는 **사용자의 검색 활동 분포를 보여줍니다.**

검색 활동 분석의 목적:

- 사용자가 콘텐츠를 **직접 탐색하는지**
- 추천 시스템을 **얼마나 활용하는지**

히스토그램을 사용하는 이유:

- 사용자 검색 행동의 **전체 분포를 파악하기 위해**

분석 포인트:

- 검색 활동이 낮으면 **추천 시스템 의존도가 높을 가능성**
- 검색 활동이 높으면 **콘텐츠 탐색 니즈가 높은 사용자 존재**

이 분석은 **콘텐츠 탐색 UX 개선 및 추천 시스템 전략에 활용될 수 있습니다.**
""")

    fig = px.histogram(
        df,
        x=search_col,
        nbins=30
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------
# User Engagement Segmentation
# -------------------------------------------------

if user_col and watch_col:

    st.subheader("👥 User Engagement Segmentation")

    st.markdown("""
사용자를 **시청 시간 기준으로 세 그룹으로 분류한 분석입니다.**

사용자 세그먼트:

- **Low Engagement** : 플랫폼 이용이 낮은 사용자
- **Medium Engagement** : 일반적인 사용자
- **High Engagement** : 플랫폼 핵심 사용자

세그먼트 분석을 사용하는 이유:

- 사용자 행동을 **단순 평균으로 설명하기 어렵기 때문**
- **핵심 사용자 그룹을 식별하기 위해**

활용 가능 전략:

- High 사용자 → VIP 관리 및 개인화 추천
- Medium 사용자 → engagement 증가 전략
- Low 사용자 → 이탈 방지 전략
""")

    user_watch = df.groupby(user_col)[watch_col].sum().reset_index()

    user_watch["segment"] = pd.qcut(
        user_watch[watch_col],
        q=3,
        labels=["Low","Medium","High"]
    )

    segment_count = user_watch["segment"].value_counts()

    fig = px.pie(
        values=segment_count.values,
        names=segment_count.index
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------
# Top Active Users
# -------------------------------------------------

if user_col and watch_col:

    st.subheader("🔥 Top Active Users")

    st.markdown("""
플랫폼에서 **가장 활발하게 활동한 사용자 상위 10명**을 분석합니다.

Bar chart를 사용하는 이유:

- 사용자별 활동량 비교가 쉽기 때문

분석 목적:

- 플랫폼 이용이 **특정 사용자에게 집중되는지 확인**
- **heavy user 의존도 분석**

Heavy User 분석은 다음 전략에 활용될 수 있습니다:

- VIP 사용자 관리
- 개인화 추천 강화
- 프리미엄 서비스 설계
""")

    top_users = (
        df.groupby(user_col)[watch_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig = px.bar(
        x=top_users.values,
        y=top_users.index,
        orientation="h"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------
# Data Preview
# -------------------------------------------------

st.subheader("📋 Data Preview")

st.markdown("""
분석에 사용된 데이터 일부를 확인할 수 있습니다.

이를 통해:

- 데이터 구조 확인
- 변수 이해
- 분석 결과 해석 지원
""")

st.dataframe(df.head(50), use_container_width=True)
