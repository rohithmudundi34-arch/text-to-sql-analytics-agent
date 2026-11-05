from langchain_ollama import ChatOllama

MODEL_NAME = "qwen2.5-coder:3b"


def get_llm():
    return ChatOllama(
        model=MODEL_NAME,
        temperature=0
    )


def generate_business_summary(question, df):
    """
    Generate a concise business-oriented summary
    from the SQL query result.
    """

    if df is None or df.empty:
        return "No data was returned for this question."

    # Convert dataframe to a compact text representation
    data_text = df.to_string(index=False)

    prompt = f"""
You are a business data analyst.

Analyze the following query result and provide a concise
business insight.

USER QUESTION:
{question}

QUERY RESULT:
{data_text}

Instructions:

1. Identify the most important finding.
2. Mention the highest or lowest value when relevant.
3. Mention useful comparisons or trends.
4. Use exact numbers from the data.
5. Do not invent information.
6. Do not discuss SQL or programming.
7. Keep the answer between 2 and 4 sentences.
8. Write in simple professional business language.
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content.strip()