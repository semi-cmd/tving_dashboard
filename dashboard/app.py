import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="TVING Retention Dashboard",
    layout="wide"
)

# --------------------------------------------------
# TVING DARK THEME
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #151a23;
}

h1, h2, h3, h4 {
    color: white;
}

p, span, label {
    color: white;
}

.stMetric {
    background-color: #1c2330;
    padding: 20px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎬 TVING Retention Dashboard")

st.markdown("""
### OTT 사용자 행동 데이터 기반 이탈 분석 시스템

이 대시보드는 **TVING 사용자 행동 로그 데이터를 분석하여**

- 사용자 활동 패턴 분석  
- 이탈 위험 사용자 탐지  
- 마케팅 개입 대상 추천  

을 지원하는 **데이터 기반 의사결정 시스템**입니다.

왼쪽 메뉴에서 각 분석 대시보드를 확인할 수 있습니다.
""")

st.divider()

# --------------------------------------------------
# DATA LOAD
# --------------------------------------------------

feature = pd.read_csv("data/processed/feature_table.csv")
pred = pd.read_csv("data/processed/prediction_result.csv")
watch = pd.read_csv("data/raw/synthetic_watch_2025.csv")

watch["timestamp"] = pd.to_datetime(watch["timestamp"])

# --------------------------------------------------
# KPI
# --------------------------------------------------

total_users = feature["user_id"].nunique()
avg_watch = round(feature["total_watch_time"].mean(),1)
high_risk = len(pred[pred["risk_score"] > 0.7])

col1, col2, col3 = st.columns(3)

col1.metric("Total Users", f"{total_users:,}")
col2.metric("Avg Watch Time", avg_watch)
col3.metric("High Risk Users", high_risk)

st.divider()

# --------------------------------------------------
# CHURN RISK GAUGE
# --------------------------------------------------

st.subheader("⚠️ Platform Churn Risk")

avg_risk = pred["risk_score"].mean()

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_risk * 100,
    title={'text': "Average Churn Risk (%)"},
    gauge={
        'axis': {'range': [0,100]},
        'bar': {'color': "#ff003c"},
        'steps': [
            {'range':[0,40],'color':"#1c2330"},
            {'range':[40,70],'color':"#2c3e50"},
            {'range':[70,100],'color':"#ff003c"}
        ]
    }
))

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# VIEWING ACTIVITY TREND
# --------------------------------------------------

st.subheader("📈 Platform Viewing Activity")

daily_views = watch.groupby(
    watch["timestamp"].dt.date
).size().reset_index(name="views")

fig2 = px.line(
    daily_views,
    x="timestamp",
    y="views",
    markers=True
)

fig2.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --------------------------------------------------
# USER SEGMENT
# --------------------------------------------------

st.subheader("👥 User Segment")

feature["segment"] = pd.qcut(
    feature["total_watch_time"],
    q=3,
    labels=["Light User","Medium User","Heavy User"]
)

seg = feature["segment"].value_counts().reset_index()
seg.columns = ["segment","count"]

fig3 = px.pie(
    seg,
    names="segment",
    values="count",
    color_discrete_sequence=["#636EFA","#00CC96","#EF553B"]
)

fig3.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --------------------------------------------------
# INSIGHT
# --------------------------------------------------

st.subheader("📊 Key Insight")

st.markdown("""
플랫폼 데이터를 분석한 결과 다음과 같은 특징을 확인할 수 있습니다.

**1️⃣ Heavy User 그룹이 플랫폼 시청 시간을 대부분 차지**

**2️⃣ 일부 사용자 그룹에서 높은 churn risk 존재**

**3️⃣ 특정 시간대에 시청 활동 집중**

이 분석 결과는 다음 전략에 활용할 수 있습니다.

- 개인화 추천 콘텐츠 강화  
- 이탈 위험 사용자 대상 마케팅 캠페인  
- 시청 패턴 기반 광고 노출 최적화
""")