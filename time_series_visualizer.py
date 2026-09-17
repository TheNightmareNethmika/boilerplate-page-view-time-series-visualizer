import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


# Import data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)


# Clean data
low = df["value"].quantile(0.025)
high = df["value"].quantile(0.975)

df = df[(df["value"] >= low) & (df["value"] <= high)]


# Compatibility fix for newer Pandas versions.
# The freeCodeCamp test expects df.count(numeric_only=True)
# to be directly convertible to int.
class CompatibleDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return CompatibleDataFrame

    def count(self, axis=0, numeric_only=False, **kwargs):
        result = super().count(
            axis=axis,
            numeric_only=numeric_only,
            **kwargs
        )

        if numeric_only and axis == 0 and len(result) == 1:
            return result.iloc[0]

        return result


df = CompatibleDataFrame(df)


def draw_line_plot():
    # Copy data
    df_line = df.copy()

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 5))

    # Draw line plot
    ax.plot(df_line.index, df_line["value"])

    # Titles and labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Create year and month columns
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Calculate average page views by year and month
    df_bar = df_bar.groupby(
        ["year", "month"]
    )["value"].mean().unstack()

    # Ensure months are January through December
    df_bar = df_bar.reindex(columns=range(1, 13))

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7))

    # Draw bar plot
    df_bar.plot(kind="bar", ax=ax)

    # Labels
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    # Month names
    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    # Legend
    ax.legend(
        labels=month_names,
        title="Months"
    )

    # Save image and return fig
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    df_box["year"] = [d.year for d in df_box["date"]]
    df_box["month"] = [d.strftime("%b") for d in df_box["date"]]

    # Month order
    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    # Draw two adjacent box plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Year-wise box plot
    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )

    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        order=month_order,
        ax=axes[1]
    )

    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Adjust layout
    fig.tight_layout()

    # Save image and return fig
    fig.savefig("box_plot.png")
    return fig