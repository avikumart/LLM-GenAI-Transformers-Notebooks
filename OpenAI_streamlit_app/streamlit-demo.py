import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Streamlit Demo",page_icon="⚡")

# App Title
st.title("Streamlit Demo Tutorial")

# Introduction
st.header("Welcome to the Streamlit Demo!")
st.write("This demo showcases the basics of Streamlit, including text inputs, sliders, and visualizations.")

# User Input
st.sidebar.header("User Input Section")

# Text Input
greeting_name = st.sidebar.text_input("Enter your name:", "Streamlit User")
st.sidebar.success(f"Hello, {greeting_name}!")

# Numeric Slider
age = st.sidebar.slider("Select your age:", min_value=1, max_value=100, value=25)
st.sidebar.info(f"Your age: {age}")

# Dropdown for a selection
gender = st.sidebar.selectbox("Select your gender:", ["Male", "Female", "Other"])
st.sidebar.warning(f"Gender: {gender}")

language = st.sidebar.multiselect("Languages known:", ["English", "Hindi", "Marathi","Gujarati"])
st.sidebar.warning(f"Languages known: {language}")

# Visualization
st.header("Visualizing Random Data")

# Generate random data
num_points = st.slider("Number of data points:", min_value=10, max_value=500, value=100)

st.header("Generated Data Table")

random_data = pd.DataFrame(
        {
            "X": np.random.randn(num_points),
            "Y": np.random.randn(num_points),
        }
    )

# DataFrame Display
st.write(random_data.head(10))

# Scatter plot
st.subheader("Scatter Plot")
fig, ax = plt.subplots()
ax.scatter(random_data["X"], random_data["Y"], alpha=0.6)
ax.set_title("Random Data Scatter Plot")
ax.set_xlabel("X Values")
ax.set_ylabel("Y Values")
st.pyplot(fig)

if st.button("Generate Histogram"):

    # Histogram
    st.subheader("Histogram")
    fig, ax = plt.subplots()
    ax.hist(random_data["X"], bins=20, alpha=0.7, label="X")
    ax.hist(random_data["Y"], bins=20, alpha=0.7, label="Y")
    ax.legend()
    ax.set_title("Histogram of X and Y")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

# Conclusion
st.header("Thank You!")