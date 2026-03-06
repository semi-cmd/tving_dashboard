import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚠️ Churn Risk Analysis")

# -----------------------------
# 설명
# -----------------------------

st.markdown("""
### 사용자 이탈 위험 분석

이 페이지에서는 사용자 행동 데이터를 기반으로  
**Churn Risk Prediction Model**이 계산한 이탈 위험 점수를 분석합니다.

Risk Score는 다음과 같은 사용자 행동 지표를 기반으로 계산됩니다.

- 시청 시간 (Watch Time)
- 콘텐츠 시청 횟수
- 검색 활동
- 추천 콘텐츠 상호작용

Risk Score가 높은 사용자는 **서비스를 떠날 가능성이 높은 사용자**로 간주됩니다.
""")

st.divider()

# -----------------------------
# 데이터 로드
# -----------------------------

df = pd.read_csv("data/processed/prediction_result.csv")

# -----------------------------
# KPI
# -----------------------------

avg_risk = df["risk_score"].mean()
high_risk_users = df[df["risk_score"] > 0.7]

col1, col2 = st.columns(2)

col1.metric(
    "Average Risk Score",
    round(avg_risk,3)
)

col2.metric(
    "High Risk Users",
    len(high_risk_users)
)

st.info("""
Risk Score 해석

- **0 ~ 0.3** → 낮은 이탈 위험  
- **0.3 ~ 0.7** → 중간 위험  
- **0.7 이상** → 높은 이탈 위험
""")

st.divider()

# -----------------------------
# Risk Score Distribution
# -----------------------------

st.subheader("📊 Risk Score Distribution")

st.markdown("""
전체 사용자 Risk Score 분포를 나타냅니다.

이 그래프를 통해 플랫폼에서 **이탈 위험 사용자의 비율**을 확인할 수 있습니다.
""")

fig = px.histogram(
    df,
    x="risk_score",
    nbins=40,
    color_discrete_sequence=["#EF553B"]
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# High Risk User Table
# -----------------------------

st.subheader("🚨 High Risk Users")

st.markdown("""
Risk Score가 **0.7 이상인 사용자**는  
서비스 이탈 가능성이 높은 사용자입니다.

이 사용자 그룹은 **마케팅 개입 또는 추천 콘텐츠 전략의 주요 대상**이 될 수 있습니다.
""")

st.dataframe(high_risk_users.head(50))

st.divider()

# -----------------------------
# Risk vs Watch Time
# -----------------------------

st.subheader("📉 Risk vs Watch Time")

st.markdown("""
시청 시간과 churn risk 사이의 관계를 분석합니다.

일반적으로 **시청 시간이 낮은 사용자가 높은 churn risk를 보이는 경향**이 있습니다.
""")

if "total_watch_time" in df.columns:

    fig2 = px.scatter(
        df,
        x="total_watch_time",
        y="risk_score",
        opacity=0.6,
        color="risk_score",
        color_continuous_scale="reds"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -----------------------------
# Insight
# -----------------------------

st.subheader("📊 Insight")

st.markdown("""
분석 결과 다음과 같은 특징을 확인할 수 있습니다.

**1️⃣ 일부 사용자 그룹에서 높은 churn risk 존재**

**2️⃣ 시청 활동이 낮은 사용자에서 churn risk가 높게 나타남**

**3️⃣ churn 위험 사용자는 마케팅 개입 대상이 될 수 있음**

이 분석은 다음 단계인

- **Intervention Recommendation**
- **마케팅 캠페인 타겟팅**

전략 수립에 활용됩니다.
""")