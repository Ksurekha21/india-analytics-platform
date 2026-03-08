import plotly.express as px
import plotly.graph_objects as go
import numpy as np


# ---------- COMMON CHART STYLE ----------

def style_chart(fig):

    fig.update_layout(
        height=400,
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig


# ---------- MAIN CHART FUNCTION ----------

def create_chart(df, metric, chart_type):

    # TIME SERIES

    if chart_type == "Line Chart":
        fig = px.line(df, x="year", y=metric)
        return style_chart(fig)

    if chart_type == "Multi-Line Chart":
        fig = px.line(df, x="year", y=metric, color="district")
        return style_chart(fig)

    if chart_type == "Area Chart":
        fig = px.area(df, x="year", y=metric)
        return style_chart(fig)

    if chart_type == "Step Line":
        fig = px.line(df, x="year", y=metric, line_shape="hv")
        return style_chart(fig)

    if chart_type == "Spline":
        fig = px.line(df, x="year", y=metric, line_shape="spline")
        return style_chart(fig)

    # COMPARISON

    if chart_type == "Bar Chart":
        fig = px.bar(df, x="year", y=metric)
        return style_chart(fig)

    if chart_type == "Horizontal Bar":
        fig = px.bar(df, y="year", x=metric, orientation="h")
        return style_chart(fig)

    if chart_type == "Grouped Bar":
        fig = px.bar(df, x="year", y=metric, color="district", barmode="group")
        return style_chart(fig)

    if chart_type == "Stacked Bar":
        fig = px.bar(df, x="year", y=metric, color="district", barmode="stack")
        return style_chart(fig)

    if chart_type == "100% Stacked":
        fig = px.bar(df, x="year", y=metric, color="district", barmode="relative")
        return style_chart(fig)

    # DISTRIBUTION

    if chart_type == "Histogram":
        fig = px.histogram(df, x=metric)
        return style_chart(fig)

    if chart_type == "Box Plot":
        fig = px.box(df, y=metric)
        return style_chart(fig)

    if chart_type == "Density Plot":
        fig = px.density_contour(df, x="year", y=metric)
        return style_chart(fig)

    if chart_type == "Violin Plot":
        fig = px.violin(df, y=metric)
        return style_chart(fig)

    # BUSINESS ANALYTICS

    if chart_type == "Pareto Chart":

        sorted_df = df.sort_values(metric, ascending=False)

        fig = go.Figure()

        fig.add_bar(
            x=sorted_df["district"],
            y=sorted_df[metric],
            name="Value"
        )

        fig.add_scatter(
            x=sorted_df["district"],
            y=np.cumsum(sorted_df[metric]) / sorted_df[metric].sum() * 100,
            name="Cumulative %",
            yaxis="y2"
        )

        fig.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right"
            )
        )

        return style_chart(fig)

    if chart_type == "Control Chart":

        mean = df[metric].mean()

        fig = px.line(df, x="year", y=metric)

        fig.add_hline(y=mean)

        return style_chart(fig)

    if chart_type == "Waterfall Chart":

        fig = go.Figure(go.Waterfall(
            x=df["year"],
            y=df[metric]
        ))

        return style_chart(fig)

    if chart_type == "Funnel Chart":

        fig = px.funnel(df, x=metric, y="year")

        return style_chart(fig)

    # DEFAULT

    fig = px.line(df, x="year", y=metric)

    return style_chart(fig)
