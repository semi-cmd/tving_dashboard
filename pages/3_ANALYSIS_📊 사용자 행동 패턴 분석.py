import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Viewing Time Pattern Analysis")

# ---------------------------------------------------
# 설명
# ---------------------------------------------------

st.markdown("""
### 사용자 시청 시간 패턴 분석

이 페이지에서는 **TVING 사용자들이 언제 콘텐츠를 가장 많이 시청하는지** 분석합니다.

OTT 플랫폼에서는 사용자 활동 시간 패턴이 다음과 같은 전략에 활용됩니다.

- 광고 노출 타이밍 최적화
- 추천 콘텐츠 노출 전략
- 푸시 알림 발송 시간 결정

이를 통해 **사용자 engagement를 높이고 churn 위험을 낮출 수 있습니다.**
""")

st.divider()

# ---------------------------------------------------
# 데이터 로드
# ---------------------------------------------------

watch = pd.read_csv("data/raw/synthetic_watch_2025.csv")

watch["timestamp"] = pd.to_datetime(watch["timestamp"])

watch["weekday"] = watch["timestamp"].dt.day_name()
watch["hour"] = watch["timestamp"].dt.hour

# ---------------------------------------------------
# Viewing Heatmap
# ---------------------------------------------------

st.subheader("🔥 Viewing Activity Heatmap")

st.markdown("""
요일과 시간대별 콘텐츠 시청 활동을 나타냅니다.

Heatmap을 통해 **사용자가 가장 활발하게 콘텐츠를 소비하는 시간대**를 확인할 수 있습니다.
""")

heatmap_data = watch.groupby(["weekday","hour"]).size().reset_index(name="views")

pivot = heatmap_data.pivot(
    index="weekday",
    columns="hour",
    values="views"
).fillna(0)

weekday_order = [
    "Monday","Tuesday","Wednesday",
    "Thursday","Friday","Saturday","Sunday"
]

pivot = pivot.reindex(weekday_order)

fig = px.imshow(
    pivot,
    labels=dict(x="Hour of Day", y="Day of Week", color="View Count"),
    aspect="auto",
    color_continuous_scale="reds"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------
# Peak Viewing Hour
# ---------------------------------------------------

st.subheader("⏰ Peak Viewing Hour")

hourly_views = watch.groupby("hour").size().reset_index(name="views")

peak_hour = hourly_views.loc[hourly_views["views"].idxmax()]["hour"]

st.success(f"📺 사용자 시청 활동이 가장 높은 시간: {peak_hour}:00")

st.divider()

# ---------------------------------------------------
# Hourly Viewing Trend
# ---------------------------------------------------

st.subheader("📈 Hourly Viewing Trend")

st.markdown("""
시간대별 콘텐츠 시청 활동 변화를 보여줍니다.

이 그래프를 통해 **사용자 활동이 증가하는 시간대**를 확인할 수 있습니다.
""")

fig2 = px.line(
    hourly_views,
    x="hour",
    y="views",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------------------------------------------
# Insight
# ---------------------------------------------------

st.subheader("📊 Insight")

st.markdown("""
시청 시간 패턴 분석 결과 다음과 같은 특징을 확인할 수 있습니다.

**1️⃣ 특정 시간대에 시청 활동 집중**

**2️⃣ 저녁 시간대 사용자 engagement 증가**

**3️⃣ 일부 시간대에서는 시청 활동 감소**

이 분석 결과는 다음 전략에 활용될 수 있습니다.

- 사용자 활동이 높은 시간대에 광고 노출 증가  
- 추천 콘텐츠 노출 강화  
- 시청 감소 시간대 푸시 알림 발송
""")