import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression

# Load environment variables from .env file immediately on startup
load_dotenv()

# Import custom utilities
from utils.parser import parse_statement
from utils.categorizer import categorize_transactions_llm
from utils.analyzer import detect_anomalies, generate_savings_plan
from utils.visualizer import plot_spending_pie, plot_spending_trend

st.set_page_config(page_title="FinSight AI Dashboard", layout="wide", page_icon="📊")

st.title("📊 FinSight AI — Intelligent Financial Advisor")
st.write("Upload your bank statements to run AI categorization, anomaly analysis, and custom forecast modeling.")

# Sidebar status configuration
st.sidebar.header("System Status")
if os.environ.get("GEMINI_API_KEY"):
    st.sidebar.success("🔒 Gemini API Key loaded from .env")
else:
    st.sidebar.error("❌ No API Key found in .env file.")
    st.sidebar.info("Please ensure you have a .env file in the root directory containing: GEMINI_API_KEY=your_key")

# File Uploader component
uploaded_file = st.file_uploader("Upload Bank Statement (CSV or PDF)", type=["csv", "pdf"])

if uploaded_file is not None:
    with st.spinner("Parsing Statement data..."):
        file_bytes = uploaded_file.read()
        try:
            df = parse_statement(file_bytes, uploaded_file.name)
            st.success("File parsed successfully!")
        except Exception as e:
            st.error(f"Error parsing file: {e}")
            st.stop()

    # Trigger AI processing
    with st.spinner("AI Categorization in progress..."):
        df['category'] = categorize_transactions_llm(df['description'].tolist())
    
    # --- DASHBOARD LAYOUT KPI METRICS ---
    st.markdown("### 📈 Monthly Summary Metrics")
    total_income = df[df['amount'] > 0]['amount'].sum()
    total_expense = df[df['amount'] < 0]['amount'].sum()
    net_savings = total_income + total_expense # expense is negative
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Spending", f"${abs(total_expense):,.2f}")
    col3.metric("Net Cash Flow", f"${net_savings:,.2f}", delta=f"${net_savings:,.2f}")
    
    st.markdown("---")
    
    # --- VISUALIZATIONS ---
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.plotly_chart(plot_spending_pie(df), use_container_width=True)
    with col_chart2:
        st.plotly_chart(plot_spending_trend(df), use_container_width=True)
        
    st.markdown("---")
    
    # --- DETECT UNUSUAL EXPENSES & ADVISORY ---
    st.markdown("### 🚨 AI Financial Health Insights")
    
    col_anom, col_plan = st.columns([1, 1])
    
    with col_anom:
        st.subheader("Detected Unusual Expenses")
        anomalies = detect_anomalies(df)
        if not anomalies.empty:
            st.warning(f"Found {len(anomalies)} suspicious or uniquely large expenses:")
            st.dataframe(anomalies[['date', 'description', 'amount']])
        else:
            st.success("No extreme spending anomalies detected this period.")
            
    with col_plan:
        st.subheader("AI Customized Savings Plan")
        if st.button("Generate Dynamic Savings Blueprint"):
            with st.spinner("Consulting AI Financial Assistant..."):
                plan = generate_savings_plan(df)
                st.info(plan)
                
    st.markdown("---")
    
    # --- FORECASTING ENGINE ---
    st.markdown("### 🔮 Future Spending Predictor")
    st.write("Using a Linear Regression model to forecast your daily compound rolling spending trend over the next 15 days.")
    
    # Preprocessing for historical regression trends
    expenses_df = df[df['amount'] < 0].copy()
    expenses_df['amount'] = expenses_df['amount'].abs()
    expenses_df['date_ordinal'] = expenses_df['date'].map(pd.Timestamp.toordinal)
    
    if len(expenses_df) > 1:
        X = expenses_df[['date_ordinal']].values
        y = expenses_df['amount'].values
        
        # Fit Sci-Kit Learn Regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict ahead
        last_date = expenses_df['date'].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=15)
        future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
        predictions = model.predict(future_ordinals)
        predictions = np.clip(predictions, a_min=0, a_max=None) # Expenses can't drop below 0
        
        # Build Forecast visual frame
        forecast_df = pd.DataFrame({'Date': future_dates, 'Forecasted Spend Amount': predictions})
        st.dataframe(forecast_df.style.format({'Forecasted Spend Amount': '${:,.2f}'}))
    else:
        st.info("Not enough individual spending occurrences to calculate a reliable machine learning regression trajectory.")