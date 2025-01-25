import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

def parse_states_and_count(event_text):
    # Overall cumulative count
    pattern_total = re.search(r'(\d+)\s+positive', event_text)
    total_count = int(pattern_total.group(1)) if pattern_total else 0
    # Extract per-state counts
    pattern_states = r'(Michigan|Texas|South Dakota|Massachusetts|Kansas|Minnesota|Colorado)\s*\((\d+)\)'
    matched_states = re.findall(pattern_states, event_text)
    state_map = {
        "Michigan": "MI", "Texas": "TX", "South Dakota": "SD", "Massachusetts": "MA",
        "Kansas": "KS", "Minnesota": "MN", "Colorado": "CO"
    }
    state_counts = []
    for name, count_str in matched_states:
        abbr = state_map.get(name, name)
        state_counts.append((abbr, int(count_str)))
    return total_count, state_counts

def main():
    st.title("Disease Dashboard")
    df = pd.read_csv("H5N1_US_2024.csv")
    df["Date_Event"] = pd.to_datetime(df["Date_Event"], errors="coerce")

    # Sidebar for category selection (default to Poultry if present)
    categories = df["Category"].unique().tolist()
    default_index = categories.index("Poultry") if "Poultry" in categories else 0
    selected_category = st.sidebar.selectbox("Select Category", categories, index=default_index)

    # Filter by category
    filtered_df = df[df["Category"] == selected_category]

    # Build data for the selected category
    data_rows = []
    for _, row in filtered_df.iterrows():
        total_count, state_counts = parse_states_and_count(row["Event"])
        for abbrev, count in state_counts:
            data_rows.append({
                "Date_Event": row["Date_Event"].date(),
                "State": abbrev,
                "Cumulative_Count": count
            })
    map_df = pd.DataFrame(data_rows)

    if map_df.empty:
        st.write("No data for this category.")
        return

    # Base choropleth
    fig_choro = px.choropleth(
        map_df,
        locations="State",
        locationmode="USA-states",
        color="Cumulative_Count",
        scope="usa",
        animation_frame="Date_Event",
        range_color=(0, map_df["Cumulative_Count"].max()),
        title=f"Progression Over Time: {selected_category}"
    )

    # Scatter for numeric labels
    fig_text = px.scatter_geo(
        map_df,
        locations="State",
        locationmode="USA-states",
        scope="usa",
        text="Cumulative_Count",
        animation_frame="Date_Event",
        color_discrete_sequence=["rgba(0,0,0,0)"],
        hover_name="State"
    )

    # Merge animation frames
    combined_fig = go.Figure(
        data=fig_choro.data,
        layout=fig_choro.layout,
        frames=fig_choro.frames
    )
    for i, scatter_frame in enumerate(fig_text.frames):
        combined_fig.frames[i].data += scatter_frame.data
    for trace in fig_text.data:
        combined_fig.add_trace(trace)
    combined_fig.layout.updatemenus = fig_text.layout.updatemenus

    st.plotly_chart(combined_fig)

if __name__ == "__main__":
    main()