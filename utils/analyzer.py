import os
import pandas as pd
from google import genai

def detect_anomalies(df):
    """
    Flags individual expenses that are significantly higher than average.
    """
    expenses = df[df['amount'] < 0].copy()
    if expenses.empty:
        return pd.DataFrame()
    
    q3 = expenses['amount'].quantile(0.25)
    q1 = expenses['amount'].quantile(0.75)
    iqr = q1 - q3
    threshold = q3 - (1.5 * iqr)
    
    anomalies = expenses[expenses['amount'] <= threshold]
    return anomalies

def generate_savings_plan(df):
    """
    Passes summarized financial data to Gemini to get tailored saving strategies.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Please provide a Gemini API key in the sidebar to generate an AI savings plan."

    # Initialize client dynamically
    client = genai.Client(api_key=api_key)
    
    summary_df = df.groupby('category')['amount'].sum().to_string()
    
    prompt = f"""
    You are an expert personal financial advisor. Analyze this monthly spending breakdown (negative numbers represent spending, positive represent income):
    
    {summary_df}
    
    Provide a comprehensive, bulleted Savings Plan. Point out where they are overspending and give 3 actionable steps to save money next month. Keep it constructive and highly personalized.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Could not generate savings plan at this time. Error: {e}"