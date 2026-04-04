import streamlit as st
import pandas as pd
import plotly.express as px
from agent import analyze_query, load_data

st.set_page_config(
    page_title='Pharma Maintenance Intelligence Agent',
    page_icon='🏭',
    layout='wide'
)

st.title('🏭 Pharma Maintenance Intelligence Agent')
st.caption('Powered by Google Gemini 1.5 Flash | GxP-Compliant AI Analysis')

df = load_data()
st.success(f'✅ Loaded {len(df)} breakdown records')

col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Records', len(df))
col2.metric('Equipment Types', df['equipment_type'].nunique())
col3.metric('Plants Covered', df['plant'].nunique())
col4.metric('Failure Categories', df['failure_type'].nunique())

st.divider()

fig = px.bar(df['failure_type'].value_counts().reset_index(),
             x='failure_type', y='count',
             title='Breakdown Frequency by Failure Type',
             color='count', color_continuous_scale='Teal')
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader('🤖 Ask the Maintenance Intelligence Agent')

qcol1, qcol2, qcol3 = st.columns(3)
q1 = qcol1.button('🔴 Critical Equipment Risk')
q2 = qcol2.button('📊 Top Failure Patterns')
q3 = qcol3.button('🔧 Preventive Maintenance Plan')

if q1:
    user_q = 'Which equipment has highest breakdown risk?'
elif q2:
    user_q = 'What are top 3 failure patterns and root causes?'
elif q3:
    user_q = 'Recommend a 30-day preventive maintenance schedule.'
else:
    user_q = ''

user_input = st.text_area('Or type your question:', value=user_q, height=100)

if st.button('🚀 Analyze with AI', type='primary') and user_input:
    with st.spinner('Gemini is analyzing your pharma data...'):
        result = analyze_query(user_input, df)
    st.success('Analysis Complete!')
    st.markdown(result)
    st.download_button('📥 Download Report', result,
                       file_name='maintenance_analysis.txt')

with st.expander('📋 View Raw Data'):
    st.dataframe(df, use_container_width=True)
