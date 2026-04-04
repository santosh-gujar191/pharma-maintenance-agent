import os
import pandas as pd
import google.generativeai as genai

try:
    import streamlit as st
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def load_data(filepath='pharma_breakdown_data.csv'):
    return pd.read_csv(filepath)

def get_data_summary(df):
    return f"Records:{len(df)}, Plants:{df['plant'].nunique()}, Top failure:{df['failure_type'].value_counts().idxmax()}, Repeats:{df['recurrence'].sum()}"

def analyze_query(question, df):
    summary = get_data_summary(df)
    prompt = f"""Pharma Maintenance AI Agent. GxP compliant. GAMP5, ICH Q10.
Data: {summary}
Failures: {df['failure_type'].value_counts().to_dict()}
Downtime: {df.groupby('equipment_type')['downtime_hours'].sum().to_dict()}
Question: {question}
Give structured answer: 1.Direct Answer 2.Root Cause 3.GxP Actions 4.Prevention"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
