import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def display_data_visualization(df):
    st.markdown("<h2 class='subheader'>Data Visualization</h2>", unsafe_allow_html=True)

    

    col1, col2 = st.columns([1, 2])  

    with col1:
        graph_type = st.selectbox("Select Graph Type", ["Select", "Line Plot", "Bar Plot", "Scatter Plot", "Histogram"])

        x_axis = None
        y_axis = None

        if graph_type == "Line Plot":
            continuous_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            x_axis = st.selectbox("Select X Axis (Continuous)", continuous_columns)
            y_axis = st.selectbox("Select Y Axis (Continuous)", continuous_columns)

            line_style = st.selectbox("Select Line Style", ["-", "--", "-.", ":"])
            line_color = st.color_picker("Select Line Color", "#1f77b4")

        elif graph_type == "Bar Plot":
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
            continuous_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            x_axis = st.selectbox("Select X Axis (Categorical)", categorical_columns)
            y_axis = st.selectbox("Select Y Axis (Continuous)", continuous_columns)

            bar_color = st.color_picker("Select Bar Color", "#1f77b4")

        elif graph_type == "Scatter Plot":
            continuous_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            x_axis = st.selectbox("Select X Axis (Continuous)", continuous_columns)
            y_axis = st.selectbox("Select Y Axis (Continuous)", continuous_columns)

            marker_style = st.selectbox("Select Marker Style", ["o", "s", "D", "^", "x"])
            marker_color = st.color_picker("Select Marker Color", "#1f77b4")

        elif graph_type == "Histogram":
            continuous_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            x_axis = st.selectbox("Select X Axis (Continuous)", continuous_columns)

            num_bins = st.slider("Select Number of Bins", min_value=5, max_value=100, value=30)
            hist_color = st.color_picker("Select Histogram Color", "#1f77b4")

        if st.button("Generate Graph"):
            # Create the plot in the second column
            with col2:
                plt.figure(figsize=(10, 5))

                if graph_type == "Line Plot":
                    plt.plot(df[x_axis], df[y_axis], linestyle=line_style, color=line_color, marker='o')
                    plt.title(f"Line Plot of {y_axis} vs {x_axis}")
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)
                    plt.grid(True)
                    plt.legend([y_axis], loc='upper left')
                    st.pyplot(plt)

                elif graph_type == "Bar Plot":
                    plt.bar(df[x_axis].astype(str), df[y_axis], color=bar_color)
                    plt.title(f"Bar Plot of {y_axis} vs {x_axis}")
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)
                    plt.xticks(rotation=45) 
                    plt.grid(axis='y')
                    st.pyplot(plt)

                elif graph_type == "Scatter Plot":
                    plt.scatter(df[x_axis], df[y_axis], marker=marker_style, color=marker_color)
                    plt.title(f"Scatter Plot of {y_axis} vs {x_axis}")
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)
                    plt.grid(True)
                    st.pyplot(plt)

                elif graph_type == "Histogram":
                    plt.hist(df[x_axis], bins=num_bins, color=hist_color, alpha=0.7)
                    plt.title(f"Histogram of {x_axis}")
                    plt.xlabel(x_axis)
                    plt.ylabel("Frequency")
                    plt.grid(axis='y')
                    st.pyplot(plt)

