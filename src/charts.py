import pandas as pd
import plotly.express as px


def create_chart(df):

    if df.empty:
        return None

    df = df.dropna(
        axis=1,
        how="all"
    )

    numeric_columns = (
        df
        .select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )

    categorical_columns = (
        df
        .select_dtypes(
            exclude="number"
        )
        .columns
        .tolist()
    )

    # ---------------------------------
    # Category + Numeric
    # ---------------------------------

    if (
        categorical_columns
        and numeric_columns
    ):

        x = categorical_columns[0]
        y = numeric_columns[0]

        if len(df) <= 30:

            return px.bar(
                df,
                x=x,
                y=y,
                title=f"{y} by {x}"
            )

    # ---------------------------------
    # Numeric + Numeric
    # ---------------------------------

    if len(numeric_columns) >= 2:

        return px.scatter(
            df,
            x=numeric_columns[0],
            y=numeric_columns[1],
            title=(
                f"{numeric_columns[1]} "
                f"vs "
                f"{numeric_columns[0]}"
            )
        )

    return None