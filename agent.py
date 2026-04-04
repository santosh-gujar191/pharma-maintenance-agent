import os
import pandas as pd
import google.generativeai as genai

key_line = open(os.path.expanduser('~/pharma-agent/.env')).read().strip()
api_key = key_line.split('=', 1)[1]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def load_data(filepath='pharma_breakdown_data.csv'):
    return pd.read_csv(filepath)

def get_data_summary(df):
    return f"""Records:{len(df)}, Plants:{df['plant'].nunique()}, Top failure:{df['failure_type'].value_counts().idxmax()}, Repeat failures:{df['recurrence'].sum()}"""

def analyze_query(question, df):
    summary = get_data_summary(df)
    prompt = f"""Pharma Maintenance AI. Data summary: {summary}. Top failures: {df['failure_type'].value_counts().to_dict()}. Equipment downtime: {df.groupby('equipment_type')['downtime_hours'].sum().to_dict()}. Question: {question}. Give brief GxP-compliant answer with root cause and recommendations."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
