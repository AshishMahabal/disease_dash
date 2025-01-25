import streamlit as st
import pandas as pd

def main():
    st.title("Disease Dashboard")
    df = pd.read_csv("H5N1_US_2024.csv")
    st.subheader("CSV Preview")
    st.dataframe(df.head())

    # Convert date column to datetime
    df["Date_Event"] = pd.to_datetime(df["Date_Event"], errors="coerce")

    # Display a simple timeline grouped by category
    st.subheader("Event Timeline by Category")
    for cat in df["Category"].unique():
        st.markdown(f"### {cat}")
        subset = df[df["Category"] == cat].sort_values("Date_Event")
        for _, row in subset.iterrows():
            st.write(f"{row['Date_Event'].date()}: {row['Event']}")

if __name__ == "__main__":
    main()