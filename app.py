import streamlit as st

from src.langgraph_agent import run_langgraph_agent
from src.database import get_schema
from src.charts import create_chart
from src.llm import generate_business_summary


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Sales Analytics Agent",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("📊 AI Sales Analytics Agent")

st.markdown(
    """
    Ask questions about your sales database using natural language.

    **Powered by Qwen2.5-Coder + Ollama + LangGraph + SQLite**
    """
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🗄️ Database")

    if st.button("Show Database Schema"):

        st.code(
            get_schema(),
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


# =========================================================
# QUESTION INPUT
# =========================================================

question = st.text_input(
    "Ask a business question",
    placeholder="Example: What are the top 5 products by revenue?"
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🚀 Analyze",
    type="primary",
    use_container_width=True
):

    # -----------------------------------------------------
    # Validate question
    # -----------------------------------------------------

    if not question.strip():

        st.warning("Please enter a question.")
        st.stop()


    # =====================================================
    # RUN LANGGRAPH AGENT
    # =====================================================

    with st.spinner(
        "🤖 LangGraph agent is analyzing your question..."
    ):

        try:

            result = run_langgraph_agent(
                question
            )

        except Exception as error:

            st.error(
                "The AI agent encountered an error."
            )

            st.exception(error)

            st.stop()


    # =====================================================
    # FAILURE HANDLING
    # =====================================================

    if not result["success"]:

        st.error(
            "❌ Query could not be completed."
        )

        st.error(
            result.get(
                "error",
                "Unknown error"
            )
        )


        # ---------------------------------------------
        # Execution History
        # ---------------------------------------------

        st.subheader(
            "🔄 Agent Execution History"
        )

        for item in result.get(
            "history",
            []
        ):

            with st.expander(
                item.get(
                    "stage",
                    "Agent Step"
                )
            ):

                st.write(item)

        st.stop()


    # =====================================================
    # GET DATA
    # =====================================================

    df = result["data"]


    # =====================================================
    # GENERATED SQL
    # =====================================================

    st.subheader(
        "🔍 Generated SQL"
    )

    st.code(
        result["sql"],
        language="sql"
    )


    # =====================================================
    # METRICS
    # =====================================================

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
            "SQL Attempts",
            result["attempts"]
        )


    # =====================================================
    # QUERY RESULTS
    # =====================================================

    st.subheader(
        "📋 Query Results"
    )

    st.dataframe(
        df,
        use_container_width=True
    )


    # =====================================================
    # DOWNLOAD RESULTS
    # =====================================================

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        "⬇️ Download Results as CSV",
        csv,
        "query_results.csv",
        "text/csv"
    )


    # =====================================================
    # VISUALIZATION
    # =====================================================

    st.subheader(
        "📈 Visualization"
    )

    try:

        chart = create_chart(
            df
        )

        if chart is not None:

            st.plotly_chart(
                chart,
                use_container_width=True
            )

        else:

            st.info(
                "No suitable chart could be generated."
            )

    except Exception as error:

        st.warning(
            "Chart generation failed."
        )

        st.exception(error)


    # =====================================================
    # AI BUSINESS INSIGHTS
    # =====================================================

    st.subheader(
        "🤖 AI Business Insights"
    )

    with st.spinner(
        "🤖 Generating business insights..."
    ):

        try:

            summary = generate_business_summary(
                question,
                df
            )

            st.info(
                summary
            )

        except Exception as error:

            st.warning(
                "AI business summary could not be generated."
            )

            st.exception(error)


    # =====================================================
    # BASIC DATA INSIGHTS
    # =====================================================

    st.subheader(
        "📊 Data Summary"
    )

    st.write(
        f"The query returned **{len(df)} rows** "
        f"across **{len(df.columns)} columns**."
    )

    numeric_columns = (
        df.select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )

    for column in numeric_columns:

        average = df[column].mean()

        st.write(
            f"**{column}** average: "
            f"{average:,.2f}"
        )


    # =====================================================
    # LANGGRAPH EXECUTION HISTORY
    # =====================================================

    with st.expander(
        "🧠 View LangGraph Execution History"
    ):

        for item in result.get(
            "history",
            []
        ):

            st.write(item)