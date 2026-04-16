import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time
from streamlit_autorefresh import st_autorefresh

def animate_value(target):
    placeholder = st.empty()
    
    if target == 0:
        placeholder.markdown(f"<div class='card-value'>0</div>", unsafe_allow_html=True)
        return
    
    step = max(1, target // 20)

    for i in range(0, target, step):
        placeholder.markdown(
            f"<div class='card-value'>{i}</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.005)

    placeholder.markdown(
        f"<div class='card-value'>{target}</div>",
        unsafe_allow_html=True
    )
st.set_page_config(layout="wide")

# ---------------------------
# DARK UI STYLE (UPGRADED)
# ---------------------------
st.markdown("""
<style>

/* 🔥 KPI CARD FIX */
[data-testid="column"] {
    background: linear-gradient(145deg, #0f172a, #1e293b);
    padding: 15px;
    border-radius: 16px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.6);
}
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
}
.card {
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(145deg, #0f172a, #1e293b);
    box-shadow: 0px 6px 20px rgba(0,0,0,0.6);
    height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 10px 25px rgba(0,0,0,0.8);
}

.section {
    padding:15px;
    border-radius:16px;
    background: linear-gradient(145deg, #0f172a, #1e293b);
    box-shadow: 0px 6px 20px rgba(0,0,0,0.6);
    min-height: 320px;   /* 🔥 equal height cards */
}
            
.card-title {
    font-size: 14px;
    color: #94a3b8;
}

.card-value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}

.status-low { color: #22c55e; }
.status-mid { color: #facc15; }
.status-high { color: #ef4444; }

</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD DATA
# ---------------------------
import os

file_path = os.path.join("output", "final_data.csv")
if "df" not in st.session_state:
    base_df = pd.read_csv(file_path)

    base_df['timestamp'] = pd.to_datetime("2024-01-01") + pd.to_timedelta(
        np.random.randint(0, 86400, size=len(base_df)), unit='s'
    )

    base_df = base_df.sort_values('timestamp')

    chunk_size = 1200
    base_df['patient_id'] = (base_df.index // chunk_size) + 1
    base_df['patient_id'] = base_df['patient_id'].apply(lambda x: f"Patient {x}")

    st.session_state.df = base_df

df = st.session_state.df
st.sidebar.title("🧑‍⚕️ Controls")

mode = st.sidebar.radio(
    "Select Mode",
    ["👩‍⚕️ Doctor Mode", "🧑‍💻 Admin Mode"]
)

patients = df['patient_id'].unique().tolist()
selected_patient = st.sidebar.selectbox("Select Patient", patients)
# ---------------------------
# ACTIVITY CONTROL (FIXED)
# ---------------------------

all_activities = df['activity'].unique().tolist()

# 🔥 Initialize ONLY ON FIRST LOAD
if "selected_activities" not in st.session_state:
    st.session_state.selected_activities = all_activities.copy()

# Multiselect controlled by session state
selected_activities = st.sidebar.multiselect(
    "Select Activities",
    all_activities,
    key="selected_activities"
)
filtered_df = df[
    (df['patient_id'] == selected_patient) &
    (df['activity'].isin(selected_activities))
]
if filtered_df.empty:
    filtered_df = df[df['patient_id'] == selected_patient]

score = filtered_df['behavior_score'].mean()
high_risk = (filtered_df['risk_level'] == "High Risk").sum()

def get_status(score):
    if score > 1:
        return "🟢 Stable"
    elif score > 0:
        return "🟡 Moderate"
    else:
        return "🔴 High Risk"

status = get_status(score)

# ---------------------------
# PREMIUM HEADER
# ---------------------------

st.markdown(f"""
<div style="
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(135deg, #1e293b, #0f172a);
    box-shadow: 0px 6px 20px rgba(0,0,0,0.6);
    margin-bottom: 20px;
">
    <h2 style="margin:0;">🏥 Elderly Care Monitoring System</h2>
    <p style="margin:0; color:#94a3b8;">
        Monitoring: <b>{selected_patient}</b> • Real-time behavior analytics
    </p>
</div>
""", unsafe_allow_html=True)
# ---------------------------
# KPI CARDS (FIXED)
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

if "Stable" in status:
    status_class = "status-low"
elif "Moderate" in status:
    status_class = "status-mid"
else:
    status_class = "status-high"

# ---------------------------
# CARD 1
# ---------------------------
with col1:
    st.markdown("<div class='card-title'>📊 Total Observations</div>", unsafe_allow_html=True)
    animate_value(len(filtered_df))

# ---------------------------
# CARD 2
# ---------------------------
with col2:
    st.markdown("<div class='card-title'>🩺 Patient Condition</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='card-value {status_class}'>{status}</div>",
        unsafe_allow_html=True
    )

# ---------------------------
# CARD 3
# ---------------------------
with col3:
    st.markdown("<div class='card-title'>🏃 Activity Types</div>", unsafe_allow_html=True)
    animate_value(filtered_df['activity'].nunique())

# ---------------------------
# CARD 4
# ---------------------------
with col4:
    st.markdown("<div class='card-title'>🚨 High Risk Events</div>", unsafe_allow_html=True)
    animate_value(high_risk)

st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
# ---------------------------
# ALERT SYSTEM (UPGRADED)
# ---------------------------
if high_risk > 100:
    alert_html = """
    <div style="padding:12px 18px; border-radius:12px; background:#7f1d1d; color:white; width:fit-content;">
    🚨 Critical Alert
    </div>
    """
elif high_risk > 20:
    alert_html = """
    <div style="padding:12px 18px; border-radius:12px; background:#78350f; color:white; width:fit-content;">
    ⚠️ Moderate Risk
    </div>
    """
else:
    alert_html = """
    <div style="padding:12px 18px; border-radius:12px; background:#064e3b; color:white; width:fit-content;">
    ✅ Stable
    </div>
    """

st.markdown(alert_html, unsafe_allow_html=True)

# ---------------------------
# CHARTS
# ---------------------------
col1, col2, col3 = st.columns(3)

# ---------------------------
# Activity Distribution
# ---------------------------
with col1:
    with st.container():
        st.markdown("#### 📊 Activity Distribution")

        counts = filtered_df['activity'].value_counts().reset_index()
        counts.columns = ['activity', 'count']

        fig = px.bar(counts, x='activity', y='count', color='count')
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Behavior Trend
# ---------------------------
with col2:
    with st.container():
        st.markdown("#### 📈 Behavior Trend")

        fig = px.line(filtered_df.head(500), x='timestamp', y='behavior_score')
        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Anomaly Detection
# ---------------------------
with col3:
    with st.container():
        st.markdown("#### 🚨 Anomaly Detection")

        subset = filtered_df.head(300)

        fig = px.scatter(
            subset,
            x=subset.index,
            y='behavior_score',
            color=subset['risk_level']
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)
# ---------------------------
# TIME ANALYSIS
# ---------------------------
st.markdown("### ⏱ Activity Pattern")

hourly = filtered_df.groupby(filtered_df['timestamp'].dt.hour)['behavior_score'].mean().reset_index()
hourly.columns = ['hour', 'behavior_score']

fig = px.line(hourly, x='hour', y='behavior_score', markers=True)
fig.update_layout(template="plotly_dark")
fig.update_xaxes(dtick=1)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# MODE SECTION
# ---------------------------
if mode == "👩‍⚕️ Doctor Mode":
    st.markdown("### 🧠 Clinical Insights")
    st.info(f"""
    Most common activity: {filtered_df['activity'].mode()[0]}  
    Average score: {round(score,2)}  
    High risk events: {high_risk}
    """)

else:
    st.markdown("### 📊 Admin Analytics")
    st.dataframe(filtered_df.head(50))
    st.write(filtered_df.describe())

# ---------------------------
# PATIENT COMPARISON
# ---------------------------
st.markdown("### 🧑‍⚕️ Patient Comparison")

patient_summary = df.groupby('patient_id')['behavior_score'].mean().reset_index()
fig = px.bar(patient_summary, x='patient_id', y='behavior_score', color='behavior_score')
fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)