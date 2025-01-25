import streamlit as st
import pandas as pd
import plotly.express as px
import re

def parse_states_and_count(event_text):
    # 1) Parse the overall cumulative count (e.g. "5 positive")
    match_total = re.search(r'(\d+)\s+positive', event_text)
    total_count = int(match_total.group(1)) if match_total else 0

    # 2) Parse each state's cumulative count in parentheses (e.g. "Michigan (2)")
    pattern = r'(Michigan|Texas|South Dakota|Massachusetts|Kansas|Minnesota|Colorado)\s*\((\d+)\)'
    matched_states = re.findall(pattern, event_text)

    # Map full state names to abbreviations (used by Plotly or your own logic)
    state_map = {
        "Michigan": "MI",
        "Texas": "TX",
        "South Dakota": "SD",
        "Massachusetts": "MA",
        "Kansas": "KS",
        "Minnesota": "MN",
        "Colorado": "CO"
    }

    # Convert each matched state to (abbrev, count) tuples
    state_counts = []
    for state_name, count_str in matched_states:
        abbr = state_map.get(state_name, state_name)
        state_counts.append((abbr, int(count_str)))

    return total_count, state_counts

def main():
    st.title("Disease Dashboard")
    df = pd.read_csv("H5N1_US_2024.csv")
    df["Date_Event"] = pd.to_datetime(df["Date_Event"], errors="coerce")

    # Build a DataFrame for the map
    data_rows = []
    for _, row in df.iterrows():
        if row["Category"] == "Poultry":
            total_count, state_counts = parse_states_and_count(row["Event"])
            for st_abbrev, count in state_counts:
                data_rows.append({
                    "Date_Event": row["Date_Event"].date(),
                    "State": st_abbrev,
                    "Cumulative_Count": count
                })
    map_df = pd.DataFrame(data_rows)

    # Create choropleth
    fig = px.choropleth(
        map_df,
        locations="State",
        color="Cumulative_Count",
        locationmode="USA-states",
        scope="usa",
        animation_frame="Date_Event",
        range_color=(0, map_df["Cumulative_Count"].max()),
        title="Progression of Poultry Cases Over Time"
    )
    st.plotly_chart(fig)

    # Print cases for Colorado and Minnesota
    co_mn_df = map_df[map_df["State"].isin(["CO", "MN"])]
    st.write("Colorado (CO) and Minnesota (MN) parsed rows:")
    st.write(co_mn_df)

if __name__ == "__main__":
    main()