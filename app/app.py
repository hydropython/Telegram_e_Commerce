import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os

# Function to load and process the .conll file
@st.cache_data
def load_data(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        st.error(f"The file {file_path} does not exist.")
        return pd.DataFrame(columns=['Token', 'Label'])

    # Read the file
    tokens = []
    labels = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue  # Skip empty lines
            else:
                # Split the line into token and label
                # Since tokens may contain spaces, we need to be careful
                # We'll assume that the label is the last element in the line
                parts = line.rsplit(' ', 1)
                if len(parts) == 2:
                    token, label = parts
                    tokens.append(token)
                    labels.append(label)
                else:
                    # Handle cases where the line does not split into token and label
                    st.warning(f"Line skipped (could not parse): '{line}'")
                    continue

    # Create DataFrame
    data = pd.DataFrame({'Token': tokens, 'Label': labels})
    return data

# File path for the .conll file
file_path = "../Data/labeled_data_freemarket_final.conll"

# Load the data
data = load_data(file_path)

# Check if data is loaded
if data.empty:
    st.error("No data loaded. Please check the file path and contents.")
else:
    # Display the first few rows of the dataframe
    st.title("Label Distribution Histogram")
    st.subheader("Labeled Data Preview")
    st.write(data.head())

    # Count occurrences of each label
    label_counts = data['Label'].value_counts()

    # Display the counts
    st.subheader("Counts of Labels")
    st.write(label_counts)

    # Create histogram with modern colors
    st.subheader("Label Counts Histogram")
    fig, ax = plt.subplots()
    label_counts.plot(kind='bar', ax=ax, color='#1f77b4')
    ax.set_title("Count of Labels", fontsize=16, fontweight='bold')
    ax.set_xlabel("Labels", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add gridlines for better readability

    # Annotate bars with counts
    for i, count in enumerate(label_counts.values):
        ax.text(i, count + max(label_counts.values)*0.01, str(count), ha='center', fontsize=12)

    st.pyplot(fig)

    # Additional information
    st.write("The histogram above displays the counts of all labels from the dataset.")