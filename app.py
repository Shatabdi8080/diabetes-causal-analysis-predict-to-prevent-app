import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ১. গবেষণালব্ধ ডেটা (DML & Economic Research)
ATE = 0.0094
# Hossain et al. (2023) অনুযায়ী বার্ষিক গড় OOP খরচ প্রায় ২৫,৪৭৩ টাকা
ANNUAL_SAVINGS_ESTIMATE = 25473 

# ২. পেজ সেটিংস ও প্রিমিয়াম থিম
st.set_page_config(page_title="Predict-to-Prevent: AI Dashboard", layout="wide", page_icon="🩺")

st.markdown("""
    <style>
    .main { background-color: #F0F4F8; } /* Light Clinical Blue-Grey */
    .header-card { background-color: #1A365D; color: white; padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 20px; }
    .report-header { background-color: #FFFFFF; padding: 10px; border-radius: 8px; border-left: 6px solid #2B6CB0; margin-top: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-bottom: 3px solid #2B6CB0; }
    </style>
    """, unsafe_allow_html=True)

# ৩. ল্যাঙ্গুয়েজ টগল (Sidebar)
lang = st.sidebar.radio("Language / ভাষা", ["English", "বাংলা"])

# ৪. সাইডবার ইনপুট
with st.sidebar:
    st.header("Patient Profile / রোগীর তথ্য")
    age = st.slider("Age / বয়স", 18, 100, 35)
    gender = st.selectbox("Gender / লিঙ্গ", ["Male", "Female"] if lang == "English" else ["পুরুষ", "মহিলা"])
    residence = st.selectbox("Residence / এলাকা", ["Urban", "Rural"])
    htn = st.radio("Hypertension / উচ্চ রক্তচাপ", ["Yes", "No"])
    
    st.markdown("---")
    st.subheader("Anthropometric Data")
    weight = st.number_input("Weight (kg) / ওজন", value=80.0)
    c1, c2 = st.columns(2)
    with c1: feet = st.number_input("Feet", value=5, min_value=3)
    with c2: inches = st.number_input("Inches", value=6, min_value=0, max_value=11)
    
    # BMI ক্যালকুলেশন ও সাইডবারে প্রদর্শন
    height_m = ((feet * 12) + inches) * 0.0254
    current_bmi = weight / (height_m ** 2)
    
    st.markdown(f"### Current BMI: <span style='color:#ff6e40'>{current_bmi:.2f}</span>", unsafe_allow_html=True)
    if current_bmi < 18.5: st.warning("Underweight")
    elif 18.5 <= current_bmi < 25: st.success("Normal Weight")
    elif 25 <= current_bmi < 30: st.warning("Overweight")
    else: st.error("Obese")

# ৫. মেইন ড্যাশবোর্ড হেডার
if lang == "English":
    title_text = "Predict-to-Prevent: Causal AI Dashboard"
    subtitle_text = "Evidence-Based Intelligence for National Diabetes Control & Economic Savings"
else:
    title_text = "প্রেডিক্ট-টু-প্রিভেন্ট: কজাল এআই ড্যাশবোর্ড"
    subtitle_text = "জাতীয় ডায়াবেটিস নিয়ন্ত্রণ ও অর্থনৈতিক সাশ্রয় নিশ্চিতে তথ্য-ভিত্তিক সমাধান"

st.markdown(f"""
    <div class='header-card'>
        <h1>{title_text}</h1>
        <p style='font-size: 1.1em; font-weight: 300;'>{subtitle_text}</p>
    </div>
    """, unsafe_allow_html=True)

# ৬. সিমুলেশন স্লাইডার
st.subheader(" Evidence-Based Risk Mitigation Simulation")
loss_goal = st.select_slider("Select weight loss goal (kg):", options=list(range(0, 21)))

if st.button("Generate Causal & Economic Report"):
    # রিস্ক ক্যালকুলেশন লজিক
    base_risk = 18.0 + (current_bmi * 0.45) + (age * 0.12)
    if htn == "Yes": base_risk += 8.5
    if residence == "Urban": base_risk += 3.5

    new_weight = weight - loss_goal
    new_bmi = new_weight / (height_m ** 2)
    bmi_diff = current_bmi - new_bmi
    reduction = (bmi_diff * ATE) * 100
    future_risk = base_risk - reduction
    # ইকোনমিক সেভিংস ক্যালকুলেশন
    total_savings = bmi_diff * ANNUAL_SAVINGS_ESTIMATE

    # ৭. মেট্রিক্স প্রদর্শন
    col1, col2, col3 = st.columns(3)
    col1.metric("Present Risk Profile", f"{base_risk:.1f}%")
    col2.metric("Projected Future Risk", f"{future_risk:.1f}%", delta=f"-{reduction:.2f}%")
    col3.metric("Est. Healthcare Savings (BDT)", f"৳ {int(total_savings):,}")

    # ৮. Dual-Axis Line Graph
    st.markdown("---")
    st.markdown("###  Visual Comparison: Risk Trajectory vs BMI")
    
    stages = ["Present State", "Goal State"]
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=stages, y=[base_risk, future_risk], name="Risk (%)", 
                   mode='lines+markers+text', text=[f"{base_risk:.1f}%", f"{future_risk:.1f}%"],
                   textposition="top center", line=dict(color="#38A169", width=4)),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=stages, y=[current_bmi, new_bmi], name="BMI Level", 
                   mode='lines+markers+text', text=[f"{current_bmi:.1f}", f"{new_bmi:.1f}"],
                   textposition="bottom center", line=dict(color="#2B6CB0", width=4)),
        secondary_y=True,
    )

    fig.update_layout(title_text="<b>Causal Impact Analysis</b>", template="plotly_white",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_yaxes(title_text="<b>Diabetes Risk (%)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>BMI Level</b>", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

    # ৯. ইনসাইট ও ইকোনমিক জাস্টিফিকেশন
    st.info(f" **Causal Insight:** Reducing BMI by {bmi_diff:.2f} units lowers the risk of diabetes by {reduction:.2f}% according to our DML model.")
    st.success(f" **Economic Value:** This lifestyle change can potentially save BDT {int(total_savings):,} in annual out-of-pocket costs.")
      

    # --- নতুন অংশ: National Population Impact ---
    st.markdown("---")
    st.header(" National Population Impact")
    
    # পপুলেশন ইনপুট স্লাইডার
    target_pop = st.slider("Target Population Size (e.g., 10 Million)", 
                           min_value=1000000, 
                           max_value=50000000, 
                           value=10000000, 
                           step=1000000)
    
    # ১ ইউনিট BMI কমালে জাতীয়ভাবে কত রোগী কমবে তার হিসাব
    prevented_cases = target_pop * ATE
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.metric("Potential Cases Prevented", f"{int(prevented_cases):,}")
    with col_p2:
        # জাতীয়ভাবে সম্ভাব্য সাশ্রয় (২৫,০০০ টাকা জনপ্রতি ধরে)
        total_national_savings = prevented_cases * ANNUAL_SAVINGS_ESTIMATE
        st.metric("National Savings (Annual)", f"৳ {int(total_national_savings / 10000000):,} Cr")

    st.write(f" **Policy Note:** If **{target_pop/1000000:.0f} Million** people reduce their BMI by just **1 unit**, Bangladesh could prevent approximately **{int(prevented_cases):,}** new diabetes cases annually, saving the economy over **{int(total_national_savings / 10000000):,} Crore BDT**.")

# ১০. সাইডবার ফুটার ও রেফারেন্স (আপডেটেড অংশ)
st.sidebar.markdown("---")
st.sidebar.markdown("###  Methodology")
st.sidebar.write("**Analysis Engine:** Double Machine Learning (DML)")
st.sidebar.write("**Dataset:** Bangladesh Demographic and Health Survey (BDHS)")

st.sidebar.markdown("###  Economic Basis")
st.sidebar.write("**Core Source:** Hossain et al. (2023)")
st.sidebar.write("**Validation:** BMC Public Health (2026)")
st.sidebar.caption("Evidence confirms that ~75% of diabetes costs in Bangladesh are for medicine, validating BMI-based prevention strategies.")

st.sidebar.markdown("---")
st.sidebar.caption("Strategic Tool for National Diabetes Control | 2026")
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 0.9em;">
        <strong>Disclaimer:</strong> This dashboard is a Decision Support Tool based on Causal Inference research. 
        Estimates represent statistical probabilities at the population level and should be used alongside clinical advice.
        <br>
        <em>Validated via Placebo Testing and Robustness Checks.</em>
    </div>
    """, 
    unsafe_allow_html=True
)
