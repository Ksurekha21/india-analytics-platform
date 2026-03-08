import streamlit as st

def get_filters(
    df,
    show_state=True,
    show_district=True,
    show_year=True,
    show_chart_type=True
):

    st.sidebar.markdown("## Filters")

    state = None
    district = None
    start_year = None
    end_year = None
    chart_type = None

    # ---------- STATE ----------
    if show_state:

        state = st.sidebar.selectbox(
            "Select State",
            sorted(df["state"].unique())
        )

    # ---------- DISTRICT ----------
    if show_district:

        if state:
            state_df = df[df["state"] == state]
            district_list = sorted(state_df["district"].unique())
        else:
            district_list = sorted(df["district"].unique())

        district = st.sidebar.selectbox(
            "Select District",
            district_list
        )

    # ---------- YEAR ----------
    if show_year:

        start_year = st.sidebar.selectbox(
            "Start Year",
            sorted(df["year"].unique())
        )

        end_year = st.sidebar.selectbox(
            "End Year",
            sorted(df["year"].unique())
        )

    # ---------- METRIC ----------
    metrics = [c for c in df.columns if c not in ["state","district","year"]]

    metric = st.sidebar.selectbox(
        "Metric",
        metrics
    )

    # ---------- CHART TYPE ----------
    if show_chart_type:

        chart_types = [
        "Line Chart","Multi-Line Chart","Area Chart","Step Line","Spline",
        "Bar Chart","Horizontal Bar","Grouped Bar","Stacked Bar","100% Stacked",
        "Histogram","Box Plot","Density Plot","Violin Plot",
        "Pareto Chart","Control Chart","Waterfall Chart","Funnel Chart"
        ]

        chart_type = st.sidebar.selectbox(
            "Chart Type",
            chart_types
        )

    analyze = st.sidebar.button("Analyze")

    return state,district,start_year,end_year,metric,chart_type,analyze