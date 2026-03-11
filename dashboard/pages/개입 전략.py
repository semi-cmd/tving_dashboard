import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎯 Intervention Recommendation")

# ---------------------------------------------------
# 설명
# ---------------------------------------------------

st.markdown("""
### 사용자 개입 전략 추천

이 페이지에서는 **Churn Risk 분석 결과를 기반으로  
마케팅 개입 대상 사용자를 추천**합니다.

Intervention Score는 다음 요소를 고려하여 계산됩니다.

- Churn Risk Score
- 사용자 활동 수준
- 콘텐츠 이용 패턴

이 점수를 통해 **마케팅 개입 우선순위 사용자 그룹**을 식별할 수 있습니다.
""")

st.divider()

# ---------------------------------------------------
# 데이터 로드
# ---------------------------------------------------

df = pd.read_csv("data/processed/intervention_result.csv")

# ---------------------------------------------------
# KPI
# ---------------------------------------------------

avg_intervention = df["intervention_score"].mean()

high_priority = df[df["intervention_score"] > 0.7]

col1, col2 = st.columns(2)

col1.metric(
    "Average Intervention Score",
    round(avg_intervention,3)
)

col2.metric(
    "High Priority Users",
    len(high_priority)
)

st.info("""
Intervention Score 해석

- **0 ~ 0.3** → 개입 필요 낮음  
- **0.3 ~ 0.7** → 개입 고려  
- **0.7 이상** → 마케팅 개입 추천 사용자
""")

st.divider()

# ---------------------------------------------------
# Top Intervention Targets
# ---------------------------------------------------

st.subheader("🔥 Top Intervention Targets")

st.markdown("""
Intervention Score가 높은 사용자 그룹입니다.

이 사용자들은 **이탈 위험이 높고 개입 효과가 클 가능성이 높은 사용자**입니다.
""")

top_users = df.sort_values(
    "intervention_score",
    ascending=False
)

st.dataframe(top_users.head(50))

st.divider()

# ---------------------------------------------------
# Risk vs Intervention Score
# ---------------------------------------------------

st.subheader("📊 Risk vs Intervention Score")

st.markdown("""
Churn Risk와 Intervention Score 관계를 분석합니다.

그래프 오른쪽 위 영역의 사용자들은  
**이탈 위험이 높고 개입 우선순위가 높은 사용자**입니다.
""")

fig = px.scatter(
    df,
    x="risk_score",
    y="intervention_score",
    opacity=0.6,
    color="intervention_score",
    color_continuous_scale="reds"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------
# User Drill-down
# ---------------------------------------------------

st.subheader("🔍 User Drill-down")

st.markdown("""
특정 사용자의 행동 데이터를 확인할 수 있습니다.

이를 통해 개별 사용자 수준의 churn risk와  
개입 필요성을 분석할 수 있습니다.
""")

user_id = st.selectbox(
    "Select User",
    df["user_id"].unique()
)

user_data = df[df["user_id"] == user_id]

st.dataframe(user_data)

st.divider()

# ---------------------------------------------------
# Insight
# ---------------------------------------------------

st.subheader("📊 Insight")

st.markdown("""
분석 결과 다음과 같은 특징을 확인할 수 있습니다.

**1️⃣ 일부 사용자 그룹에서 높은 Intervention Score 존재**

**2️⃣ 높은 churn risk 사용자 중 일부는 마케팅 개입 효과가 높을 가능성 존재**

**3️⃣ 개입 우선순위를 통해 마케팅 비용을 효율적으로 사용할 수 있음**

이 분석은 다음 전략에 활용될 수 있습니다.

- 개인화 추천 콘텐츠 제공  
- 프로모션 및 할인 캠페인  
- 푸시 알림 기반 사용자 리텐션 전략
""")
