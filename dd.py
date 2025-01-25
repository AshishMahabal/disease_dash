import streamlit as st
import pandas as pd

def main():
    st.title("Disease Dashboard")
    df = pd.read_csv("H5N1_US_2024.csv")
    st.subheader("CSV Preview")
    st.dataframe(df.head())

    # Convert date column to datetime
    df["Date_Event"] = pd.to_datetime(df["Date_Event"], errors="coerce")

    # Sidebar selection for Category
    category_list = sorted(df["Category"].unique())
    selected_category = st.sidebar.selectbox("Select Category", category_list)

    # Display timeline only for the selected category
    st.subheader(f"Event Timeline for {selected_category}")
    subset = df[df["Category"] == selected_category].sort_values("Date_Event")
    for _, row in subset.iterrows():
        st.write(f"{row['Date_Event'].date()}: {row['Event']}")

if __name__ == "__main__":
    main()