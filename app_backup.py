import streamlit as st

from src.agent import run_agent
from src.database import get_schema
from src.charts import create_chart


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Sales Analytics Agent",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("📊 AI Sales Analytics Agent")

st.markdown(
    """
    Ask questions about your sales database using natural language.

    **Powered by Gemini + SQLite**
    """
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("🗄️ Database")

    if st.button("Show Database Schema"):

        schema = get_schema()

        st.code(
            schema,
            language="text"
        )

    st.divider()

    st.header("💡 Example Questions")

    examples = [
        "What are the top 5 products by revenue?",
        "Which city generated the highest revenue?",
        "Show monthly sales revenue.",
        "What is revenue by category?",
        "Who are the top 5 customers by revenue?"
    ]

    for example in examples:
        st.write("• " + example)


# ---------------------------------------------------------
# QUESTION INPUT
# ---------------------------------------------------------

question = st.text_input(
    "Ask a business question",
    placeholder="Example: What are the top 5 products by revenue?"
)


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

if st.button(
    "🚀 Analyze",
    type="primary",
    use_container_width=True
):

    if not question.strip():

        st.warning("Please enter a question.")

        st.stop()


    # -----------------------------------------------------
    # RUN AI AGENT
    # -----------------------------------------------------

    with st.spinner(
        "🤖 AI is generating and executing SQL..."
    ):

        try:

            result = run_agent(question)

        except Exception as error:

            st.error(
                "The AI agent encountered an error."
            )

            st.exception(error)

            st.stop()


    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------

    if not result["success"]:

        st.error(
            "❌ Query could not be completed."
        )

        st.write(
            "Error:",
            result["error"]
        )

        st.subheader("🔄 Agent Attempts")

        for attempt in result["attempts"]:

            st.write(
                f"Attempt {attempt['attempt']}"
            )

            st.code(
                attempt["sql"],
                language="sql"
            )

            st.error(
                attempt["error"]
            )

        st.stop()


    # -----------------------------------------------------
    # GENERATED SQL
    # -----------------------------------------------------

    st.subheader("🔍 Generated SQL")

    st.code(
        result["sql"],
        language="sql"
    )


    # -----------------------------------------------------
    # QUERY RESULTS
    # -----------------------------------------------------

    df = result["data"]

    st.subheader("📋 Query Results")

    st.dataframe(
        df,
        use_container_width=True
    )


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Rows",
            len(df)
        )

    with col2:

        st.metric(
            "Columns",
            len(df.columns)
        )

    with col3:

        st.metric(
            "Attempts",
            len(result["attempts"]) + 1
        )


    # -----------------------------------------------------
    # CSV DOWNLOAD
    # -----------------------------------------------------

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv,
        file_name="query_results.csv",
        mime="text/csv"
    )


    # -----------------------------------------------------
    # CHART
    # -----------------------------------------------------

    st.subheader("📈 Visualization")

    try:

        chart = create_chart(df)

        if chart is not None:

            st.plotly_chart(
                chart,
                use_container_width=True
            )

        else:

            st.info(
                "No suitable chart could be generated for this result."
            )

    except Exception as error:

        st.warning(
            "Chart generation failed."
        )

        st.exception(error)


    # -----------------------------------------------------
    # BASIC INSIGHTS
    # -----------------------------------------------------

    st.subheader("💡 Data Insights")

    if df.empty:

        st.info(
            "The query returned no data."
        )

    else:

        st.write(
            f"The query returned **{len(df)} rows** "
            f"and **{len(df.columns)} columns**."
        )

        numeric_columns = (
            df.select_dtypes(include="number")
            .columns
            .tolist()
        )

        if numeric_columns:

            for column in numeric_columns:

                average = df[column].mean()

                st.write(
                    f"**{column}** average: "
                    f"{average:,.2f}"
                )