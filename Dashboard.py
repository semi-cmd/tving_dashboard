import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# ----------------------------
# TITLE
# ----------------------------

st.title("📺 TVING Product Analytics Dashboard")

st.divider()

# ----------------------------
# WORKFLOW
# ----------------------------

st.subheader("전체 분석 프로세스")

c1,c2,c3,c4,c5,c6,c7 = st.columns(7)

c1.markdown("➡ 서비스 상태")
c2.markdown("➡ 위험 사용자 발견")
c3.markdown("➡ 세그먼트 분석")
c4.markdown("➡ 이탈 원인 분석")
c5.markdown("➡ Push 전략")
c6.markdown("➡ A/B Test")
c7.markdown("➡ 결과 분석")

st.divider()

# ----------------------------
# KPI
# ----------------------------

k1,k2,k3,k4 = st.columns(4)

k1.metric("이탈 위험 사용자", "18%", "+4%")
k2.metric("Retention", "76.4%", "-1.2%")
k3.metric("24h 재방문율", "42.1%", "+6%")
k4.metric("평균 시청 시간", "47분")

st.divider()

# ------------------------------------------------
# RISK TREND + SEGMENT
# ------------------------------------------------

left, right = st.columns([3,2])   # ← 비율 조정

# ------------------------------------------------
# 위험 사용자 추이
# ------------------------------------------------

with left:

    st.subheader("위험 사용자 추이 (주차별)")
    st.caption("디바이스별 이탈 위험 사용자 비율 변화")

    trend = pd.DataFrame({
        "week":["W01","W02","W03","W04","W05","W06","W07","W08"],
        "전체":[11,12,12,13,13,15,16,18],
        "Mobile":[12,13,12,14,14,16,17,19],
        "TV":[10,11,12,12,14,16,18,23],
        "Web":[9,10,10,11,11,12,13,14]
    })

    fig = px.line(
        trend,
        x="week",
        y=["전체","Mobile","TV","Web"],
        markers=True
    )

    fig.update_layout(
        height=320,   # ← 그래프 높이 줄임
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
        legend_title=""
    )

    st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------
# 사용자 세그먼트
# ------------------------------------------------

# ------------------------------------------------
# 사용자 세그먼트
# ------------------------------------------------

with right:

    st.subheader("사용자 세그먼트 분포")
    st.caption("참여도 기준 4단계 분류")

    seg_left, seg_right = st.columns([1,1])

    # -------------------
    # 도넛 차트
    # -------------------

    with seg_left:

        segment = pd.DataFrame({
            "segment":["신규","적응","고몰입","위험"],
            "value":[23,35,24,18]
        })

        fig = px.pie(
            segment,
            names="segment",
            values="value",
            hole=0.65,
            color="segment",
            color_discrete_map={
                "신규":"#5DADE2",
                "적응":"#1ABC9C",
                "고몰입":"#F5B041",
                "위험":"#FF4D4D"
            }
        )

        fig.update_traces(textinfo="none")  # ← % 제거

        fig.update_layout(
            height=280,
            showlegend=False,
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="white"
        )

        st.plotly_chart(fig, use_container_width=True)


    # -------------------
    # 세그먼트 카드
    # -------------------

    with seg_right:

        c1,c2 = st.columns(2)
        c3,c4 = st.columns(2)

        with c1:
            st.markdown("🟦 **신규**")
            st.markdown("### 23%")
            st.caption("약 69만 명")

        with c2:
            st.markdown("🟢 **적응**")
            st.markdown("### 35%")
            st.caption("약 105만 명")

        with c3:
            st.markdown("🟡 **고몰입**")
            st.markdown("### 24%")
            st.caption("약 72만 명")

        with c4:
            st.markdown("🔴 **위험**")
            st.markdown("### 18%")
            st.caption("약 54만 명")

# ------------------------------------------------
# USER JOURNEY + CHURN CURVE
# ------------------------------------------------

left, right = st.columns([2,1.4])

# ------------------------------------------------
# 사용자 여정 퍼널
# ------------------------------------------------

with left:

    st.subheader("사용자 여정 퍼널")
    st.caption("유입 → 재방문까지 단계별 이탈 추적")

    journey = pd.DataFrame({
        "stage":[
            "유입",
            "홈 탐색",
            "콘텐츠 클릭",
            "재생 시작",
            "5분 이상 시청",
            "콘텐츠 완주",
            "재방문"
        ],
        "percent":[100,78,61,52,39,26,42]
    })

    for i,row in journey.iterrows():

        st.markdown(
        f"""
        <div style="margin-bottom:10px">

        <div style="display:flex;justify-content:space-between;">
        <span style="color:white">{row.stage}</span>
        <span style="color:white">{row.percent}%</span>
        </div>

        <div style="background:#222;height:14px;border-radius:6px;">
        <div style="width:{row.percent}%;
                    background:linear-gradient(90deg,#4b79a1,#283e51);
                    height:14px;border-radius:6px;">
        </div>
        </div>

        </div>
        """,
        unsafe_allow_html=True
        )

    st.info("💡 핵심 이탈 구간 : 홈 탐색 → 콘텐츠 클릭 / 5분 시청 → 완주")


# ------------------------------------------------
# 이탈 확률 Curve
# ------------------------------------------------

with right:

    st.subheader("이탈 확률 Curve & 개입 타이밍")
    st.caption("일자별 이탈 확률 변화")

    days = ["D1","D3","D5","D7","D10","D14","D21","D28","D35"]
    risk = [12,34,45,52,63,71,82,89,93]

    df = pd.DataFrame({
        "day":days,
        "risk":risk
    })

    fig = px.line(
        df,
        x="day",
        y="risk",
        markers=True
    )

    fig.update_traces(
        line_color="#ff2d55",
        marker=dict(size=8)
    )

    fig.update_layout(
        height=300,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
        yaxis_title="이탈 확률 (%)",
        xaxis_title=""
    )

    st.plotly_chart(fig,use_container_width=True)


<<<<<<< HEAD
    st.warning("🎯 최적 개입 시점 : Day 7 이전 — Push 캠페인 효과 최대")
=======
    st.warning("🎯 최적 개입 시점 : Day 7 이전 — Push 캠페인 효과 최대")
>>>>>>> f5d9d226b75825793f387768736c0a1fac8ed033
