import streamlit as st
import time

def show_notification(message, duration=3):
    notification_key = f"notification_{time.time()}"
    
    st.session_state[notification_key] = {
        "message": message,
        "visible": True
    }
    
    notification_placeholder = st.empty() 
    with notification_placeholder.container():
        st.success(message)
    
    time.sleep(duration)  
    st.session_state[notification_key]["visible"] = False 
    notification_placeholder.empty()  
