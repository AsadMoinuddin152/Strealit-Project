

import streamlit as st

def display_data_summary(df):
    st.markdown("<h2 class='subheader'>Data Summary</h2>", unsafe_allow_html=True)

    # Data Description
    st.markdown("<h4>Data Description</h4>", unsafe_allow_html=True)
    st.write(df.describe())

    # Create columns for the summaryQQA
    col1, col2, col3 = st.columns(3)

    # Null Values Count
    with col1:
        st.markdown("<h4>Null Values Count</h4>", unsafe_allow_html=True)
        null_counts = df.isnull().sum()
        st.write(null_counts[null_counts > 0])

    # Data Types
    with col2:
        st.markdown("<h4>Data Types</h4>", unsafe_allow_html=True)
        st.write(df.dtypes)

    # Unique Values Count
    with col3:
        st.markdown("<h4>Unique Values Count</h4>", unsafe_allow_html=True)
        unique_counts = df.nunique()
        st.write(unique_counts)
