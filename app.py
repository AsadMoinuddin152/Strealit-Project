#Registration Number: 24MAI0112
#Name : Asad Moinuddin


import streamlit as st
import pandas as pd
from db_utils import (
    load_postgresql_tables,
    load_postgresql_data,
    load_mongodb_collections,
    load_mongodb_data,
    load_mysql_tables,
    load_mysql_data,
)
from utils import (
    show_notification
)
from data_summary import( 
    display_data_summary
)
from data_visualization import (
    display_data_visualization
)


st.markdown("""
    <style>
        .title { text-align: center; font-size: 36px; color: #4CAF50; margin: 20px 0; font-family: 'Arial', sans-serif; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); }
        .subheader { font-size: 24px; color: #F1F1F1; font-family: 'Verdana', sans-serif; margin: 10px 0; text-align: left; }
        .dataframe { background-color: #1E1E1E; border: 1px solid #333; border-radius: 5px; padding: 10px; margin-bottom: 20px; color: #E0E0E0; }
        .no-data { font-size: 20px; color: #FF4500; text-align: center; font-family: 'Arial', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("DataViz Studio")

data_source = st.sidebar.selectbox("Select data source", ("CSV File", "Excel File", "Connect to Database"))

# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'tables' not in st.session_state:
    st.session_state.tables = []
if 'collections' not in st.session_state:
    st.session_state.collections = []
if 'collection_name' not in st.session_state:
    st.session_state.collection_name = None
if 'table_name' not in st.session_state:
    st.session_state.table_name = None
if 'db_type' not in st.session_state:
    st.session_state.db_type = None
if 'df' not in st.session_state:  
    st.session_state.df = None

if data_source == "CSV File":
    st.session_state.uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

elif data_source == "Excel File":
    st.session_state.uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

elif data_source == "Connect to Database":
    st.session_state.db_type = st.sidebar.selectbox("Select Database Type", ("PostgreSQL", "MongoDB", "MySQL"))

    if st.session_state.db_type == "PostgreSQL":
        st.sidebar.subheader("PostgreSQL Connection Details")
        db_host = st.sidebar.text_input("Host", value="localhost")
        db_port = st.sidebar.text_input("Port", value="5432")
        db_user = st.sidebar.text_input("Username")
        db_pass = st.sidebar.text_input("Password", type="password")
        db_name = st.sidebar.text_input("Database Name")

        if st.sidebar.button("Get Tables"):
            st.session_state.tables = load_postgresql_tables(db_host, db_port, db_user, db_pass, db_name)

    elif st.session_state.db_type == "MongoDB":
        st.sidebar.subheader("MongoDB Connection Details")
        mongo_uri = st.sidebar.text_input("MongoDB URI (e.g., mongodb://localhost:27017)")
        mongo_db = st.sidebar.text_input("Database Name")

        if st.sidebar.button("Get Collections"):
            st.session_state.collections = load_mongodb_collections(mongo_uri, mongo_db)

    elif st.session_state.db_type == "MySQL":
        st.sidebar.subheader("MySQL Connection Details")
        db_host = st.sidebar.text_input("Host", value="localhost")
        db_port = st.sidebar.text_input("Port", value="3306")
        db_user = st.sidebar.text_input("Username")
        db_pass = st.sidebar.text_input("Password", type="password")
        db_name = st.sidebar.text_input("Database Name")

        if st.sidebar.button("Get Tables"):
            st.session_state.tables = load_mysql_tables(db_host, db_port, db_user, db_pass, db_name)

# Table selection based on database type
if st.session_state.db_type == "PostgreSQL" and st.session_state.tables:
    st.session_state.table_name = st.sidebar.selectbox("Select Table", st.session_state.tables)

elif st.session_state.db_type == "MongoDB" and st.session_state.collections:
    st.session_state.collection_name = st.sidebar.selectbox("Select Collection", st.session_state.collections)

elif st.session_state.db_type == "MySQL" and st.session_state.tables:
    st.session_state.table_name = st.sidebar.selectbox("Select Table", st.session_state.tables)

if st.session_state.db_type in ["PostgreSQL", "MongoDB", "MySQL"]:
    num_rows = st.sidebar.selectbox("Select number of rows to retrieve", [10, 20, 50, 100, 200])

if data_source in ["CSV File", "Excel File"]:
    if st.sidebar.button("Upload"):
        if data_source == "CSV File" and st.session_state.uploaded_file is not None:
            st.session_state.df = pd.read_csv(st.session_state.uploaded_file)
            st.sidebar.success(f"File {st.session_state.uploaded_file.name} uploaded successfully!")

        elif data_source == "Excel File" and st.session_state.uploaded_file is not None:
            st.session_state.df = pd.read_excel(st.session_state.uploaded_file) 
            st.sidebar.success(f"File {st.session_state.uploaded_file.name} uploaded successfully!")

elif data_source == "Connect to Database":
    if st.sidebar.button("Get Data"):
        if st.session_state.db_type == "PostgreSQL":
            if db_host and db_port and db_user and db_pass and db_name and st.session_state.table_name:
                st.session_state.df = load_postgresql_data(num_rows, st.session_state.table_name, db_host, db_port, db_user, db_pass, db_name)
                show_notification("Connected to PostgreSQL database and data loaded!", duration=3)
                
        elif st.session_state.db_type == "MongoDB":
            if mongo_uri and mongo_db:
                st.session_state.df = load_mongodb_data(num_rows, st.session_state.collection_name, mongo_uri, mongo_db)
                show_notification("Connected to MongoDB and data loaded!", duration=3)
        
        elif st.session_state.db_type == "MySQL":
            if db_host and db_port and db_user and db_pass and db_name and st.session_state.table_name:
                st.session_state.df = load_mysql_data(num_rows, st.session_state.table_name, db_host, db_port, db_user, db_pass, db_name)
                show_notification("Connected to MySQL database and data loaded!", duration=3)

st.markdown("<h1 class='title'>DataViz Studio</h1>", unsafe_allow_html=True)

if st.session_state.df is None:
    st.markdown("<p class='no-data'>🚀 Oops! It looks like we have no data to show right now. <br> Please upload your dataset or connect to a database!</p>", unsafe_allow_html=True)
else:
    st.markdown("<h2 class='subheader'>Data Information</h2>", unsafe_allow_html=True)
    st.markdown(f"**Shape:** {st.session_state.df.shape[0]} rows, {st.session_state.df.shape[1]} columns")
    
    st.markdown("<h2 class='subheader'>Data Head</h2>", unsafe_allow_html=True)  
    st.dataframe(st.session_state.df.head(10), use_container_width=True)
    
    option = st.selectbox("Select an option", ["Select", "Data Summary", "Data Visualization"])

    if option == "Data Summary":
        display_data_summary(st.session_state.df)
    elif option == "Data Visualization":
        display_data_visualization(st.session_state.df)